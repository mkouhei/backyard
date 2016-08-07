# -*- coding: utf-8 -*-
"""backyard.inventory.views."""
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    """index."""
    return render_to_response('index.html', {'project': 'backyard'})
