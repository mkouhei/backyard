# -*- coding: utf-8 -*-
"""backyard.inventory.views.receives."""
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from ..models.product import Product
from ..models.order_history import OrderHistory
from ..models.receive_history import ReceiveHistory
from ..queryset.order_history import OrderQuerySet
from ..queryset.received_history import ReceivedQuerySet


class ReceivesView(TemplateView):
    """Receives."""
    model = ReceiveHistory

    @method_decorator(login_required)
    def get(self, request, *args):
        """receives view."""
        inventory_id = args[0]
        product_id = args[1]
        if args[3]:
            return self._show(inventory_id, product_id, args[4])
        else:
            return self._index(inventory_id, product_id)

    def _index(self, inventory_id, product_id):
        received_obj = (
            ReceiveHistory.objects
            .select_related('received_item__ordered_item__product')
            .filter(
                Q(owner=self.request.user) &
                Q(received_item__id=product_id)
            )
        )
        product = Product.objects.get(id=product_id)
        return render(self.request,
                      'products/receives/index.html',
                      {'inventory_id': inventory_id,
                       'product_id': product_id,
                       'product_name': product.name,
                       'received_items': received_obj})

    def _show(self, product_id, ordered_id):
        ordered_obj = OrderHistory.objects.get(
            Q(owner=self.request.user) &
            Q(id=ordered_id)
        )
        query = OrderQuerySet(ordered_obj)
        return render(self.request,
                      'products/orders/show.html',
                      {'ordered_item': ordered_obj,
                       'query': query})
