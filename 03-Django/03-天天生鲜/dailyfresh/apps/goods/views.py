from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner, IndexPromotionBanner, GoodsSKU
from django_redis import get_redis_connection


class IndexView(View):
    '''商品首页'''
    def get(self, request):
        context = cache.get('index_cached_data')  # 根据键名获取缓存数据，无则返回None
        if context is None:
            '''显示首页'''
            print('无缓存获，取数据')
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
            cache.set('index_cached_data', context, 60*60)  # 设置缓存：键名 值 过期时间（秒）
        # 缓存不为空
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


class DetailView(View):
    def get(self, request, sku_id):
        '''显示商品详情页'''
        # 获取种类信息
        types = GoodsType.objects.all()
        # 获取对应sku_id商品的信息
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return redirect(reverse('goods:index'))
        # 获取同spu商品信息
        others = GoodsSKU.objects.filter(goods=sku.goods).exclude(id=sku.id)
        # 获取新品推荐信息（同类商品信息）
        new_goods = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]
        # 获取购车车信息
        current_user = request.user
        if current_user.is_authenticated():
            '''用户已登录'''
            conn = get_redis_connection('default')
            cart_count = conn.hlen('cart_{0}'.format(current_user.id))
            # 更新浏览记录
            history_key = '{0}_history'.format(current_user.id)
            # 删除已有的相同记录
            conn.lrem(history_key, 0, sku.id)
            # 添加记录
            conn.lpush(history_key, sku.id)
            # 限制记录保存的条目数为5
            conn.ltrim(history_key, 0, 4)
        else:
            cart_count = 0
        # 上下文
        context = {
            'sku': sku,
            'others': others,
            'new_goods': new_goods,
            'cart_count': cart_count,
            'types': types,
            'cart_count': cart_count
        }
        return render(request, 'detail.html', context)


class ListView(View):
    '''商品列表页'''
    def get(self, request, type_id, current_page):
        # 获取分类方式
        sort = request.GET.get('sort')
        # 获取全部分类
        types = GoodsType.objects.all()
        # 获取当前类
        current_type = GoodsType.objects.get(id=type_id)
        # 获取当前类的所有商品
        goods_all = GoodsSKU.objects.filter(type=current_type).order_by('-create_time')
        # 新品推荐
        new_goods = goods_all[:2]
        # 判断分类方式
        if sort == 'sales':
            goods_all = goods_all.order_by('sales')
        elif sort == 'price':
            goods_all = goods_all.order_by('price')
        else:
            sort = 'default'
        # 构造分页器实例
        p = Paginator(goods_all, 1)
        # 获取当前页
        try:
            sub_page = p.page(current_page)
        except EmptyPage:
            # current_page超出总页数
            sub_page = p.page(p.num_pages)
        except PageNotAnInteger:
            # current_page 不是一个整数
            sub_page = p.page(1)
        # 获取分页索引列表，页码只展示前五页
        page_nums_show = 3
        page_half_show = (page_nums_show + 1) // 2
        if p.num_pages <= page_nums_show:
            # 总页数小于五页
            page_index_range = range(1, p.num_pages + 1)
        elif sub_page.number <= page_half_show:
            # 当前页码属于前三页
            page_index_range = range(1, page_nums_show + 1)
        elif sub_page.number > p.num_pages - page_half_show:
            page_index_range = range(p.num_pages - page_nums_show + 1, p.num_pages + 1)
        else:
            page_index_range = range(sub_page.number - page_half_show + 1, sub_page.number + page_half_show)
        # 获取购物车数据
        current_user = request.user
        if current_user.is_authenticated():
            '''用户已登录'''
            conn = get_redis_connection('default')
            cart_count = conn.hlen('cart_{0}'.format(current_user.id))
        else:
            cart_count = 0
        context = {
            'type': current_type,
            'types': types,
            'sub_page': sub_page,
            'cart_count': cart_count,
            'new_goods': new_goods,
            'sort': sort,
            'current_page': int(current_page),
            'page_index_range': page_index_range
        }
        return render(request, 'list.html', context)
