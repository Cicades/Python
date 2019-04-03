from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from goods.models import GoodsSKU
from django_redis import get_redis_connection


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
