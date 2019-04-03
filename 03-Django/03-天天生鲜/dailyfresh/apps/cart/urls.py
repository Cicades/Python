from django.conf.urls import url
from cart.views import  CarAddView

urlpatterns = [
    url(r'^add$', CarAddView.as_view(), name='add'),  # 添加商品
]
