from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^travels$', views.success),
    url(r'^logout$', views.logout),
    url(r'^travels/new$', views.add),
    url(r'^travels/add$', views.create),
    url(r'^travels/destination/(?P<dest_id>\d+)$', views.dest_info),
    url(r'^travels/join/(?P<trip_id>\d+)$', views.join)
]