# -*- coding: utf-8 -*-
"""backyard.inventory.queryset.product."""
from django.db.models import Sum, Q

from ..models.product import Product


class ProductQuerySet(object):
    """Quantity queries."""

    def __init__(self, product_id, group):
        """initialize."""
        self.product_id = product_id
        self.group = group

    @property
    def ordered(self):
        """ordered quantity."""
        return Product.objects.filter(
            Q(orderhistory__isnull=False) &
            Q(id=self.product_id) &
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
            Q(id=self.product_id) &
            Q(unpackhistory__group=self.group)
        )

    @property
    def quantities(self):
        return (self.ordered & self.unpacked).values().first()
