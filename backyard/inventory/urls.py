# -*- coding: utf-8 -*-
"""backyard.inventory.urls."""

from django.conf.urls import url, patterns


urlpatterns = patterns('backyard.inventory.views',
                       url(r'^$', 'index', name='index'),)
