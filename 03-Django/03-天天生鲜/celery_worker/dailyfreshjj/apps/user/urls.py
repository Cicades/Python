from django.conf.urls import url
from user.views import RegisterView


urlpatterns = [
	url(r'^register$', RegisterView.as_view())
]
