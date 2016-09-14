# -*- coding: utf-8 -*-
"""backyard.inventory.queryset.order_history."""
from django.db.models import Q

from ..models.order_history import OrderHistory


class OrderQuerySet(object):
    """Order quereis."""

    def __init__(self, product_id, group):
        """initialize."""
        self.product_id = product_id
        self.group = group
        self.order_query = OrderHistory.objects.select_related(
            'price'
        ).filter(
            Q(product_id=self.product_id) &
            Q(group=self.group)
        )

    @property
    def order(self):
        return self.order_query.values(
            'ordered_at',
            'price__price',
            'ordered_quantity',
            'received_at',
            'received_quantity',
        )

    @property
    def product_name(self):
        """product name."""
        return self.order_query.values('product__name').first().get('product__name')
