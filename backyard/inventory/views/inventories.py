# -*- coding: utf-8 -*-
"""backyard.inventory.views.inventories."""
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from ..models.product import Product


class InventoriesView(TemplateView):
    """Inventories."""
    model = Product

    @method_decorator(login_required)
    def get(self, request, *args):
        """inventories view."""
        if args[1]:
            return self._show(args[1])
        else:
            return self._index()

    def _show(self, product_id):
        return
        
    def _index(self):
        group = self.request.user.groups.first()
        ordered = Product.objects.filter(
            Q(orderhistory__isnull=False) &
            Q(orderhistory__group=group)
        ).annotate(
            ordered=Sum('orderhistory__ordered_quantity'),
            received=Sum('orderhistory__received_quantity')
        )
        unpacked = Product.objects.extra(
            select={'unpacked': 'quantity'}
        ).filter(
            Q(unpackhistory__isnull=False) &
            Q(unpackhistory__group=group)
        )
        return render(self.request,
                      'inventories/index.html',
                      {'products': (ordered & unpacked).values()})
