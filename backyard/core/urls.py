# -*- coding: utf-8 -*-
"""backyard.core.urls."""
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('backyard.inventory.urls')),
]
