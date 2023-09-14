from django.conf.urls import url
from . import views
from django.contrib import admin

#app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_seller/$', views.create_seller, name='create_seller'),
    url(r'^buyer/$', views.buyer, name='buyer'),
    url(r'^(?P<seller_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<seller_id>[0-9]+)/wishlist/$', views.wishlist, name='wishlist'),
    url(r'^wishlisted_seller/(?P<filter_by>[a-zA_Z]+)/$', views.wishlisted_seller, name='wishlisted_seller'),
    url(r'^(?P<seller_id>[0-9]+)/$', views.detail1, name='detail1'),
    url(r'^(?P<seller_id>[0-9]+)/delete_seller/$', views.delete_seller, name='delete_seller'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<seller_id>[0-9]+)/home/$', views.Home, name='home'),
    url(r'^post/$', views.Post, name='post'),
    url(r'^messages/$', views.Messages, name='messages'),
]

