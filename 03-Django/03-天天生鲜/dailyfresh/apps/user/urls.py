from django.conf.urls import url
from user.views import RegisterView, user_active, UserLogin


urlpatterns = [
	url(r'^register$', RegisterView.as_view(), name='register'),
	url(r'^active/(?P<token>.*)$', user_active, name='user_active'),
	url(r'^login$', UserLogin.as_view(), name='login')
]
