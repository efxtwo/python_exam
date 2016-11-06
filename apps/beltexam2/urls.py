from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes, name='quotes'),
    url(r'^create$', views.create, name='create'),
    url(r'user/(?P<id>\d+)/add$', views.add, name='add'),
    url(r'user/(?P<id>\d+)/remove$', views.remove, name='remove'),
    url(r'^user/(?P<id>\d+)$', views.user),


]
