# -*- coding: utf-8 -*-
"""backyard.inventory.views.dashboard."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator


class DashboardView(TemplateView):
    """Dashboard."""

    @method_decorator(login_required)
    def get(self, request):
        """dashboard index."""
        return render(request, 'dashboard/index.html')
