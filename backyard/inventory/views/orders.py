# -*- coding: utf-8 -*-
"""backyard.inventory.views.orders."""
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from backyard.inventory.models import OrderHistory
from backyard.inventory.queryset.order_history import OrderQuerySet


class OrdersView(TemplateView):
    """Orders."""
    model = OrderHistory

    @method_decorator(login_required)
    def get(self, request, *args):
        """orders view."""
        product_id = args[0]
        if args[3]:
            return self._show(product_id, args[3])
        else:
            return self._index(product_id)

    def _index(self, product_id):
        ordered_obj = OrderHistory.objects.filter(
            Q(owner=self.request.user) &
            Q(ordered_item__id=product_id)
        )
        product_name = ordered_obj[0].ordered_item.product.name
        return render(self.request,
                      'products/orders/index.html',
                      {'product_id': product_id,
                       'product_name': product_name,
                       'ordered_items': ordered_obj})

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
