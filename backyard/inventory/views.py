# -*- coding: utf-8 -*-
"""backyard.inventory.views."""
from django.shortcuts import render_to_response


def index(request):
    """index."""
    return render_to_response('index.html')


def login(request):
    """login page."""
    return render_to_response('login.html')
