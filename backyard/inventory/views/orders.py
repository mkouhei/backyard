# -*- coding: utf-8 -*-
"""backyard.inventory.views.orders."""
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from ..models.order_history import OrderHistory
from ..queryset.order_history import OrderQuerySet


class OrdersView(TemplateView):
    """Orders."""
    model = OrderHistory

    @method_decorator(login_required)
    def get(self, request, *args):
        """orders view."""
        inventory_id = args[0]
        ordered_id = args[1]
        if args[4]:
            return self._show(inventory_id, args[3])
        else:
            return self._index(inventory_id, ordered_id)

    def _index(self, inventory_id, product_id):
        ordered_obj = (
            OrderHistory.objects.select_related('ordered_item__product')
            .filter(
                Q(owner=self.request.user) &
                Q(ordered_item__product_id=product_id)
            )
        )
        product_name = OrderQuerySet(ordered_obj[0]).product_name
        return render(self.request,
                      'products/orders/index.html',
                      {'inventory_id': inventory_id,
                       'product_name': product_name,
                       'ordered_items': ordered_obj})

    def _show(self, inventory_id, ordered_id):
        ordered_obj = OrderHistory.objects.get(
            Q(owner=self.request.user) &
            Q(id=inventory_id)
        )
        query = OrderQuerySet(ordered_obj)
        return render(self.request,
                      'products/orders/show.html',
                      {'ordered_item': ordered_obj,
                       'query': query})
