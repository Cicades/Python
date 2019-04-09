from django.conf.urls import url
from user.views import RegisterView, user_active, UserLogin, UserInfoView, UserSiteView, UserOrderView, UserLogoutView


urlpatterns = [
	url(r'^register$', RegisterView.as_view(), name='register'),
	url(r'^active/(?P<token>.*)$', user_active, name='user_active'),
	url(r'^login$', UserLogin.as_view(), name='login'),
	url(r'logout$', UserLogoutView.as_view(), name='logout'),
	url(r'^info$', UserInfoView.as_view(), name='user_info'),
	url(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'),
	url(r'^site$', UserSiteView.as_view(), name='site')
]
