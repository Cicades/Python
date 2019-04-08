from django.conf.urls import url
from cart.views import  CarAddView, CartInfoView, CartUpdateView, CartDelView

urlpatterns = [
    url(r'^add$', CarAddView.as_view(), name='add'),  # 添加商品
    url(r'^info$', CartInfoView.as_view(), name='info'),
    url(r'^update$', CartUpdateView.as_view(), name='update'),
    url(r'^del$', CartDelView.as_view(), name='del')
]
