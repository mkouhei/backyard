# -*- coding: utf-8 -*-
"""backyard.inventory.views.inventories."""
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from backyard.inventory.models import Inventory
from backyard.inventory.queryset.inventory import QuantityQuerySet


class InventoriesView(TemplateView):
    """Inventories."""
    model = Inventory

    @method_decorator(login_required)
    def get(self, request, *args):
        """inventories view."""
        if args[1]:
            return self._show(args[1])
        else:
            return self._index()

    def _show(self, inventory_id):
        inventory_obj = Inventory.objects.get(
            Q(owner=self.request.user) &
            Q(id=inventory_id)
        )
        query = QuantityQuerySet(inventory_obj)
        return render(self.request,
                      'inventories/show.html',
                      {'inventory': inventory_obj,
                       'quantity': query})

    def _index(self):
        query = [(i, QuantityQuerySet(i))
                 for i in Inventory.objects.filter(owner=self.request.user)]
        return render(self.request,
                      'inventories/index.html',
                      {'inventories': query})
