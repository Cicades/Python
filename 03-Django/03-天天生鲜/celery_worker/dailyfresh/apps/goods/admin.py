from django.contrib import admin
from goods.models import Goods, GoodsType, GoodsSKU
# Register your models here.
admin.site.register(Goods)
admin.site.register(GoodsType)
admin.site.register(GoodsSKU)