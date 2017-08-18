from django.conf.urls import url

from . import views

urlpatterns=[
	url(r'^$', views.netdiag),
	url(r'^newtest', views.newtest),
	url(r'^awesome', views.awesome),
	url(r'^connection', views.connection),
]
