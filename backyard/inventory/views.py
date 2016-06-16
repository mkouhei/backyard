# -*- coding: utf-8 -*-
"""backyard.inventory.views."""
from django.shortcuts import render
from django.shortcuts import render_to_response


def index(request):
    """index."""
    return render_to_response('index.html')
