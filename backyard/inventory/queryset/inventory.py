# -*- coding: utf-8 -*-
"""backyard.inventory.queryset.inventory."""
from django.db.models import Q, Sum

from backyard.inventory.models.product import Product


class InventoryQuerySet(object):
    """Inventory query set."""

    def __init__(self, group):
        self.group = group

    @property
    def ordered(self):
        return Product.objects.filter(
            Q(orderhistory__isnull=False) &
            Q(orderhistory__group=self.group)
        ).annotate(
            ordered=Sum('orderhistory__ordered_quantity'),
            received=Sum('orderhistory__received_quantity')
        )

    @property
    def unpacked(self):
        return Product.objects.extra(
            select={'unpacked': 'quantity'}
        ).filter(
            Q(unpackhistory__isnull=False) &
            Q(unpackhistory__group=self.group)
        )
