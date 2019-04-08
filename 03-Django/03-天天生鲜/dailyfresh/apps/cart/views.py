from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from goods.models import GoodsSKU
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin


# Create your views here.
class CarAddView(View):
    """添加商品到购物车"""
    def post(self, request):
        """添加商品"""
        sku_id = request.POST.get('sku_id')
        sku_num = request.POST.get('sku_num')
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': -1, 'errmsg': '用户尚未登录！'})
        if not all([sku_num, sku_id]):
            '''数据不完整'''
            return JsonResponse({'res': 0, 'errmsg': '数据不完整！'})
        try:
            sku_num = int(sku_num)
        except ValueError:
            return JsonResponse({'res': 1, 'errmsg': '数据格式有误！'})
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 1, 'errmsg': '数据格式有误！'})
        if sku.stock < sku_num:
            return JsonResponse({'res': 2, 'errmsg': '库存不足！'})
        # 连接redis
        redis_client = get_redis_connection('default')
        h_name = 'cart_{0}'.format(user.id)
        old_count = redis_client.hget(h_name, sku_id)  # 去购物车对应sku的数量
        old_count = 0 if old_count is None else int(old_count)
        old_count += sku_num
        redis_client.hset(h_name, sku_id, old_count)
        context = {
            'res': 'OK',
            'cartCount': redis_client.hlen(h_name)
        }
        return JsonResponse(context)


class CartInfoView(LoginRequiredMixin, View):
    """展示购物车页面"""
    def get(self, request):
        user = request.user  # 登录用户
        redis_client = get_redis_connection('default')
        h_name = 'cart_{0}'.format(user.id)
        redis_cart_data = redis_client.hgetall(h_name)
        skus = list()
        goods_count = 0  # 总商品件数
        total_price = 0  # 总价
        for sku_id, sku_count in redis_cart_data.items():
            sku_id = sku_id.decode()
            sku_count = sku_count.decode()
            sku = GoodsSKU.objects.get(id=sku_id)
            skus.append(sku)
            sku.count = int(sku_count)  # sku数量
            sku.total_price = sku.count * sku.price  # 商品小计
            goods_count += sku.count  # 更新总价数
            total_price += sku.total_price  # 更新总价
        # 组织上下文
        context = {
            'skus': skus,
            'goods_count': goods_count,
            'total_price': total_price
        }
        return render(request, 'cart.html', context)


class CartUpdateView(View):
    """更新商品到购物车"""
    def post(self, request):
        """添加商品"""
        sku_id = request.POST.get('sku_id')
        sku_num = request.POST.get('sku_num')
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': -1, 'errmsg': '用户尚未登录！'})
        if not all([sku_num, sku_id]):
            '''数据不完整'''
            return JsonResponse({'res': 0, 'errmsg': '数据不完整！'})
        try:
            sku_num = int(sku_num)
        except ValueError:
            return JsonResponse({'res': 1, 'errmsg': '数据格式有误！'})
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 1, 'errmsg': '数据格式有误！'})
        if sku.stock < sku_num:
            return JsonResponse({'res': 2, 'errmsg': '库存不足！'})
        # 连接redis
        redis_client = get_redis_connection('default')
        h_name = 'cart_{0}'.format(user.id)
        redis_client.hset(h_name, sku_id, sku_num)
        context = {
            'res': 'OK',
        }
        return JsonResponse(context)


class CartDelView(View):
    """删除购物车数据"""
    def post(self, request):
        sku_id = request.POST.get('sku_id')
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '用户尚未登录'})
        if sku_id is None:
            return JsonResponse({'res': 1, 'errmsg': '数据不完整！'})
        redis_client = get_redis_connection('default')
        h_name = 'cart_{0}'.format(user.id)
        sku = redis_client.hget(h_name, sku_id)
        if sku is None:
            return JsonResponse({'res': 2, 'errmsg': '数据有误！'})
        redis_client.hdel(h_name, sku_id)

        return JsonResponse({'res': 'OK', 'errmsg': '删除成功！'})



