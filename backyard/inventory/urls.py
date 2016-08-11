# -*- coding: utf-8 -*-
"""backyard.inventory.urls."""
from django.conf.urls import url
from django.contrib.auth.views import login, logout
from backyard.inventory.views.dashboard import DashboardView
from backyard.inventory.views.inventories import InventoriesView


urlpatterns = [
    url(r'^login', login),
    url(r'^logout', logout, {'template_name': 'logout.html'}),
    url(r'^inventories(/?)(\d?)$', InventoriesView.as_view()),
    url(r'', DashboardView.as_view()),
]
