# -*- coding: utf-8 -*-
"""backyard.inventory.views.orders."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from ..queryset.order_history import OrderQuerySet


class OrdersView(TemplateView):
    """Orders."""

    @method_decorator(login_required)
    def get(self, request, *args):
        """orders view."""
        product_id = args[0]
        if args[2]:
            return self._show(product_id, args[2])
        else:
            return self._index(product_id)

    def _index(self, product_id):
        group = self.request.user.groups.first()
        query = OrderQuerySet(product_id, group)
        return render(self.request,
                      'inventories/orders/index.html',
                      {'ordered_items': query.order,
                       'product_name': query.product_name,
                       'product_id': product_id})

    def _show(self, product_id, ordered_id):
        return
