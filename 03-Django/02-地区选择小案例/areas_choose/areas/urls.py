from django.conf.urls import url
from areas import views

urlpatterns = [
	url(r'^index$', views.index),
	url(r'^get_prov$', views.get_prov),
	url(r'^get_city', views.get_city),
	url(r'^get_region', views.get_region)
]