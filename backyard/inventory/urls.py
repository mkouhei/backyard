# -*- coding: utf-8 -*-
"""backyard.inventory.urls."""
from django.conf.urls import url
from backyard.inventory import views


urlpatterns = [url(r'^', views.index)]
