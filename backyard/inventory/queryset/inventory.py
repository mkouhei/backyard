# -*- coding: utf-8 -*-
"""backyard.inventory.queryset.inventory."""
from django.db.models import Q, Sum
from backyard.inventory.models import (OrderHistory,
                                       ReceiveHistory,
                                       UnpackHistory)


class QuantityQuerySet(object):
    """Quantity queries."""

    def __init__(self, obj):
        """initialize."""
        self.obj = obj

    def ordered_item(self):
        """ordered item."""
        return OrderHistory.objects.filter(
            Q(order_item__product=self.obj.product)
        ).values('order_item__product').distinct()

    def ordered_quantity(self):
        """ordered quantity."""
        return OrderHistory.objects.filter(
            Q(order_item__product=self.obj.product)
        ).aggregate(Sum('quantity')).get('quantity__sum')

    def received_quantity(self):
        """received quantity."""
        return ReceiveHistory.objects.filter(
            Q(received_item=self.ordered_item())
        ).aggregate(Sum('quantity')).get('quantity__sum')

    def unpacked_quantity(self):
        """unpacked quantity."""
        return UnpackHistory.objects.filter(
            Q(unpacked_item=self.obj.product)
        ).aggregate(Sum('quantity')).get('quantity__sum')

    def remain_quantity(self):
        """remain quantity."""
        if self.ordered_quantity() >= self.received_quantity():
            return self.received_quantity() - self.unpacked_quantity()
        else:
            return 0
