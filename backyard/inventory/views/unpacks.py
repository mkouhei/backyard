# -*- coding: utf-8 -*-
"""backyard.inventory.views.unpacks."""
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from backyard.inventory.models import OrderHistory, UnpackHistory
from backyard.inventory.queryset.order_history import OrderQuerySet
from backyard.inventory.queryset.unpacked_history import UnpackQuerySet


class UnpacksView(TemplateView):
    """Unpacks."""
    model = UnpackHistory

    @method_decorator(login_required)
    def get(self, request, *args):
        """receives view."""
        product_id = args[0]
        if args[3]:
            return self._show(product_id, args[3])
        else:
            return self._index(product_id)

    def _index(self, product_id):
        unpacked_obj = UnpackHistory.objects.filter(
            Q(owner=self.request.user) &
            Q(unpacked_item__id=product_id)
        )
        product_name = UnpackQuerySet(unpacked_obj[0]).product_name
        return render(self.request,
                      'products/unpacks/index.html',
                      {'product_id': product_id,
                       'product_name': product_name,
                       'unpacked_items': unpacked_obj})

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
