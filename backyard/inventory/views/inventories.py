# -*- coding: utf-8 -*-
"""backyard.inventory.views.inventories."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from backyard.inventory.models import Inventory
from backyard.inventory.queryset.inventory import QuantityQuerySet


class InventoriesView(TemplateView):
    """Inventories."""
    model = Inventory

    @method_decorator(login_required)
    def get(self, request):
        """inventories view."""
        query = [(i, QuantityQuerySet(i))
                 for i in Inventory.objects.filter(owner=request.user)]
        return render(request,
                      'inventories/index.html',
                      {'inventories': query})
