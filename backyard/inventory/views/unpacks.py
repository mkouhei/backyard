# -*- coding: utf-8 -*-
"""backyard.inventory.views.unpacks."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from ..queryset.unpacked_history import UnpackQuerySet


class UnpacksView(TemplateView):
    """Unpacks."""

    @method_decorator(login_required)
    def get(self, request, *args):
        """receives view."""
        product_id = args[0]
        if args[2]:
            return self._show(product_id, args[2])
        else:
            return self._index(product_id)

    def _index(self, product_id):
        group = self.request.user.groups.first()
        query = UnpackQuerySet(product_id, group)
        return render(self.request,
                      'inventories/unpacks/index.html',
                      {'unpacked_items': query.unpack,
                       'product_name': query.product_name,
                       'product_id': product_id})

    def _show(self, product_id, ordered_id):
        return
