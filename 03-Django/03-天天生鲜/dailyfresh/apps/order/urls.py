from django.conf.urls import url
from order.views import PlaceOrderView, CommitOrderView
urlpatterns = [
    url(r'place_order', PlaceOrderView.as_view(), name='place_order'),  # 订单生成页面
    url(r'commit', CommitOrderView.as_view(), name='commit')  # 订单提交页面
]
