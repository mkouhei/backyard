# -*- coding: utf-8 -*-
"""backyard.inventory.queryset.inventory."""
from django.db.models import Q, Sum

from ..models.order_history import OrderHistory
from ..models.receive_history import ReceiveHistory
from ..models.unpack_history import UnpackHistory


class QuantityQuerySet(object):
    """Quantity queries."""

    def __init__(self, obj):
        """initialize."""
        self.obj = obj

    @property
    def ordered_item(self):
        """ordered item."""
        return OrderHistory.objects.filter(
            Q(ordered_item__product=self.obj.product) & Q(group=self.obj.group)
        )

    @property
    def ordered_quantity(self):
        """ordered quantity."""
        return OrderHistory.objects.filter(
            Q(ordered_item__product=self.obj.product) & Q(group=self.obj.group)
        ).aggregate(Sum('quantity')).get('quantity__sum')

    @property
    def received_quantity(self):
        """received quantity."""
        try:
            quantity = ReceiveHistory.objects.filter(
                Q(received_item=self.ordered_item) & Q(group=self.obj.group)
            ).aggregate(Sum('quantity')).get('quantity__sum')
            if quantity is None:
                quantity = 0
            return quantity
        except ReceiveHistory.DoesNotExist:
            return 0

    @property
    def unpacked_quantity(self):
        """unpacked quantity."""
        try:
            quantity = UnpackHistory.objects.filter(
                Q(unpacked_item=self.obj.product) & Q(group=self.obj.group)
            ).aggregate(Sum('quantity')).get('quantity__sum')
            if quantity is None:
                quantity = 0
            return quantity
        except UnpackHistory.DoesNotExist:
            return 0

    @property
    def remain_quantity(self):
        """remain quantity."""
        if self.ordered_quantity >= self.received_quantity:
            return self.received_quantity - self.unpacked_quantity
        else:
            return 0
