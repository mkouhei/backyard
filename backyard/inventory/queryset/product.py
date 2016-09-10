# -*- coding: utf-8 -*-
"""backyard.inventory.queryset.product."""
from django.db.models import Sum


class ProductQuerySet(object):
    """Quantity queries."""

    def __init__(self, obj):
        """initialize."""
        self.obj = obj

    @property
    def ordered_quantity(self):
        """ordered quantity."""
        ordered = self.obj.orderhistory_set.aggregate(ordered=Sum('ordered_quantity')).get('ordered')
        if ordered is None:
            ordered = 0
        return ordered

    @property
    def received_quantity(self):
        received = self.obj.orderhistory_set.aggregate(received=Sum('received_quantity')).get('received')
        if received is None:
            received = 0
        return received

    @property
    def unpacked_quantity(self):
        unpacked = self.obj.unpackhistory_set.aggregate(unpacked=Sum('quantity')).get('unpacked')
        if unpacked is None:
            unpacked = 0
        return unpacked

    @property
    def remain_quantity(self):
        return self.received_quantity - self.unpacked_quantity
