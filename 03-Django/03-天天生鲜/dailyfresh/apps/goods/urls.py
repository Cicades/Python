from django.conf.urls import url
from goods.views import IndexView
urlpatterns = [
    url(r'^$', view=IndexView.as_view(), name='index'),
]
