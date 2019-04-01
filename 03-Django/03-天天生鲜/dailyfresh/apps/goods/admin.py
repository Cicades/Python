from django.contrib import admin
from django.core.cache import cache
from celery_tasks.tasks import generate_static_index
from goods.models import Goods, GoodsType, GoodsSKU, GoodsImage, IndexGoodsBanner, IndexTypeGoodsBanner, IndexPromotionBanner
# Register your models here.


class BaseModelAdmin(admin.ModelAdmin):
    '''重写ModelAdmim的方法，使其在后台修改数据时，发出generate_static_index任务'''
    def save_model(self, request, obj, form, change):
        '''修改数据'''
        super(BaseModelAdmin, self).save_model(request, obj, form, change)
        generate_static_index.delay()  # 重新生成静态首页
        cache.delete('index_cached_data')  # 删除缓存

    def delete_model(self, request, obj):
        super(BaseModelAdmin, self).delete_model(request, obj)
        generate_static_index.delay()
        cache.delete('index_cached_data')  # 删除缓存


class GoodsTypeAdmin(BaseModelAdmin):
    pass


class IndexGoodsBannerAdmin(BaseModelAdmin):
    pass


class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
    pass


class IndexPromotionBannerAdmin(BaseModelAdmin):
    pass


admin.site.register(Goods)
admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
