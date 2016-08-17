# -*- coding: utf-8 -*-
"""backyard.inventory.queryset.unpacked_history."""
from django.db.models import Q, Sum

from ..models.order_history import OrderHistory
from ..models.receive_history import ReceiveHistory


class UnpackQuerySet(object):
    """Unpack queries."""

    def __init__(self, obj):
        """initialize."""
        self.obj = obj

    @property
    def product_name(self):
        """product name."""
        return self.obj.unpacked_item.name

    @property
    def ordered_quantity(self):
        """ordered quantity."""
        return OrderHistory.objects.filter(
            (Q(ordered_item__product=self.obj.unpacked_item) &
             Q(group=self.obj.group))
            ).aggregate(Sum('quantity')).get('quantity__sum')

    @property
    def received_quantity(self):
        """received quantity."""
        return ReceiveHistory.objects.filter(
            (Q(received_item__ordered_item__product=self.obj.unpacked_item) &
             Q(group=self.obj.group))
        ).aggregate(Sum('quantity')).get('quantity__sum')

    @property
    def unpacked_quantity(self):
        """unpacked quantity."""
        return self.obj.quantity

    @property
    def remain_quantity(self):
        """remain quantity."""
        if self.ordered_quantity >= self.received_quantity:
            return self.received_quantity - self.unpacked_quantity
        else:
            return 0
