# -*- coding: utf-8 -*-
"""backyard.core.urls."""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
