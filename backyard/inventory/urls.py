# -*- coding: utf-8 -*-
"""backyard.inventory.urls."""
from django.conf.urls import url
from django.contrib.auth.views import login, logout

from .views.dashboard import DashboardView
from .views.inventories import InventoriesView
from .views.orders import OrdersView
from .views.receives import ReceivesView
from .views.unpacks import UnpacksView


urlpatterns = [
    url(r'^login', login),
    url(r'^logout', logout, {'template_name': 'logout.html'}),
    url(r'^inventories(/?)(([0-9]+)?)$',
        InventoriesView.as_view()),
    url(r'^products/([0-9]+)/orders(/?)(([0-9]+)?)$',
        OrdersView.as_view()),
    url(r'^products/([0-9]+)/receives(/?)(([0-9]+)?)$',
        ReceivesView.as_view()),
    url(r'^products/([0-9]+)/unpacks(/?)(([0-9]+)?)$',
        UnpacksView.as_view()),
    url(r'^$', DashboardView.as_view()),
]
