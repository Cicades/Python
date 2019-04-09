import time
from django.shortcuts import render
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from user.models import Address
from goods.models import GoodsSKU
from order.models import OrderInfo, OrderGoods
from django_redis import get_redis_connection
from django.http import JsonResponse
from django.db import transaction
# Create your views here.


class PlaceOrderView(LoginRequiredMixin, View):
    """订单支付页面"""
    def post(self, request):
        user = request.user
        # 获取收货地址
        addrs = Address.objects.filter(user=user)
        # 获取商品
        sku_ids = request.POST.getlist('sku_id')
        redis_client = get_redis_connection('default')
        total_price = 0  # 订单总金额
        freight = 10  # 运费
        total_nums = 0  # 商品总件数
        h_name = 'cart_{0}'.format(user.id)  # redis购物车记录对应的name
        order_goods = []
        for sku_id in sku_ids:
            goods = GoodsSKU.objects.get(id=sku_id)
            count = int(redis_client.hget(h_name, sku_id))  # 商品件数
            amount = goods.price * count  # 商品小计
            total_price += amount
            total_nums += count
            goods.count = count
            goods.amount = amount
            order_goods.append(goods)
        # 组织上下文
        context = {
            'order_goods': order_goods,
            'addrs': addrs,
            'total_price': total_price,
            'total_nums': total_nums,
            'freight': freight,
            'pay_money': total_price + freight,
            'sku_ids': ','.join(sku_ids)
        }
        return render(request, 'place_order.html', context)


class CommitOrderView(View):
    """订单提交页面"""
    @transaction.atomic
    def post(self, request):
        '''
        1.由于订单创建涉及一系列sql操作，并且具有原子性，因此需开启事物来处理
        2.mysql默认事物的隔离级别是repeatable read，即在并发情况下事物a不能读取到事务b提交的内容，
        为方便乐观锁操作将其级别因设为read-committed
        '''
        addr_id = request.POST.get('addr')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('skus')
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': -1, 'errmsg': '用户尚未登录！'})
        # 完整性校验
        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({'res': 0, 'errmsg': '数据不完整！'})
        # 地址合法性校验
        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({'res': 1, 'errmsg': '收货地址不合法！'})
        # 支付方式合法性校验
        if pay_method not in OrderInfo.PAY_METHODS:
            return JsonResponse({'res': 2, 'errmsg': '支付方式不合法！'})

        # 创建订单：
        # 1.创建orderinfo
        order_id = time.strftime('%Y%m%d%H%M%S') + str(user.id)  # 订单id
        pay_method = int(pay_method)
        total_price = 0  # 订单总金额
        transit_price = 10  # 运费
        total_count = 0  # 商品总件数
        savepoint_id = transaction.savepoint()  # 创建保存点
        try:
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                addr=addr,
                pay_method=pay_method,
                total_count=total_count,
                total_price=total_price,
                transit_price=transit_price
            )
            # 2.创建ordergoods
            sku_ids = sku_ids.split(',')
            redis_client = get_redis_connection('default')
            h_name = 'cart_{0}'.format(user.id)  # redis购物车记录对应的name
            for sku_id in sku_ids:
                for i in range(3):
                    try:
                        # 悲观锁，即在事务中，进行某条sql操作时会加上for update，从而锁定相关行或者相关表，其它并发操作会堵塞
                        # goods = GoodsSKU.objects.select_for_update.get(id=sku_id)
                        goods = GoodsSKU.objects.get(id=sku_id)
                    except GoodsSKU.DoesNotExist:
                        transaction.savepoint_rollback(savepoint_id)  # 回滚
                        return JsonResponse({'res': 3, 'errmsg': '购买的商品异常！'})
                    count = redis_client.hget(h_name, sku_id)  # 商品件数
                    if count is None:
                        transaction.savepoint_rollback(savepoint_id)  # 回滚
                        return JsonResponse({'res': 4, 'errmsg': '商品不存在于购物车！'})
                    count = int(count)
                    # 判断库存
                    if count > goods.stock:
                        transaction.savepoint_rollback(savepoint_id)  # 回滚
                        return JsonResponse({'res': 5, 'errmsg': '%s库存不足！' % goods.name})
                    # 更新sku数据
                    # goods.stock -= count
                    # goods.sales += count
                    # goods.save()
                    old_stock = goods.stock
                    old_sales = goods.sales
                    # 乐观锁实现：只有当现有库存等于同一个事务的原有库存时才能更新成功
                    # 但同时也带来另外一个问题：当库存足够时，并发的事务中只有一个事务会成功，为避免此种情况的发生可以多尝试几次
                    res = GoodsSKU.objects.filter(id=sku_id, stock=old_stock)\
                        .update(stock=old_stock-count, sales=old_sales+count)  # 返回受影响行数
                    if not res:
                        if i == 2:
                            # 受影响行数为0
                            transaction.savepoint_rollback(savepoint_id)
                            return JsonResponse({'res': 6, 'errmsg': '订单生成失败!'})
                    else:
                        amount = goods.price * count  # 商品小计
                        total_price += amount
                        total_count += count
                        OrderGoods.objects.create(
                            order=order,
                            sku=goods,
                            count=count,
                            price=amount
                        )
                        break
            # 3.更新orderinfo中的数据
            order.total_count = total_count
            order.total_price = total_price
            order.save()
        except Exception as res:
            transaction.savepoint_rollback(savepoint_id)  # 回滚
            return JsonResponse({'res': 6, 'errmsg': '%s' % res})
        else:
            transaction.savepoint_commit(savepoint_id)  # 提交
            redis_client.hdel(h_name, *sku_ids)  # 删除购物车对应的商品id
            return JsonResponse({'res': 'OK', 'errmsg': '订单创建成功!'})
