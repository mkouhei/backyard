# -*- coding: utf-8 -*-
"""backyard.inventory.urls."""
from django.conf.urls import url
from django.contrib.auth.views import login, logout
from backyard.inventory import views


urlpatterns = [
    url(r'^login', login, {'template_name': 'login.html'}),
    url(r'^logout', logout, {'template_name': 'logout.html'}),
    url(r'', views.index),
]
