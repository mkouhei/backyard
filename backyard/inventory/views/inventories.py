# -*- coding: utf-8 -*-
"""backyard.inventory.views.inventories."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from ..queryset.inventory import InventoryQuerySet
from ..queryset.product import ProductQuerySet


class InventoriesView(TemplateView):
    """Inventories."""

    @method_decorator(login_required)
    def get(self, request, *args):
        """inventories view."""
        if args[1]:
            return self._show(args[1])
        else:
            return self._index()

    def _show(self, product_id):
        group = self.request.user.groups.first()
        return render(self.request,
                      'inventories/show.html',
                      {'product': ProductQuerySet(product_id, group).quantities})
        
    def _index(self):
        group = self.request.user.groups.first()
        return render(self.request,
                      'inventories/index.html',
                      {'products': InventoryQuerySet(group).quantities})
