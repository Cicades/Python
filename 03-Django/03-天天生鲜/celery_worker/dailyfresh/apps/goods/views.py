from django.shortcuts import render
from django.views.generic import View
from goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner, IndexPromotionBanner
from django_redis import get_redis_connection


class IndexView(View):
    '''商品首页'''
    def get(self, request):
        '''显示首页'''
        # 轮播图左边的商品分类
        types = GoodsType.objects.all()
        # 轮播图
        carousels = IndexGoodsBanner.objects.all().order_by('index')
        # 轮播图右边的活动
        promotions = IndexPromotionBanner.objects.all().order_by('index')
        # 轮播图下方的同类商品list
        for type in types:
            all_goods = IndexTypeGoodsBanner.objects.filter(type=type)
            type.text_show = all_goods.filter(display_type=0).order_by('index')  # 用文字做展示的商品
            type.img_show = all_goods.filter(display_type=1).order_by('index')  # 用图片作展示的商品
        context = {
            'types': types,
            'carousel': carousels,
            'promotions': promotions,
        }
        # 如果用户处于登录状态则还应获取购物车的商品数
        '''
        为了加快数据的处理速度，采用redis来存储购物数据
        购物车记录设计：
        key: cart_<user_id>  value: {'goods_sku_id': goods_num}
        '''
        current_user = request.user
        if current_user.is_authenticated():
            '''用户已登录'''
            conn = get_redis_connection('default')
            cart_count = conn.hlen('cart_{0}'.format(current_user.id))
        else:
            cart_count = 0
        context['cart_count'] = cart_count
        return render(request, 'index.html', context)
