# -*- coding: utf-8 -*-
"""backyard.inventory.queryset.inventory."""
from django.db.models import Q, Sum



class QuantityQuerySet(object):
    """Quantity queries."""

    def __init__(self, obj):
        """initialize."""
        self.obj = obj

    @property
    def ordered_item(self):
        """ordered item."""
        return (
            self.obj.product.pricehistory_set.select_related().
            filter(orderhistory__quantity__gt=0).
            values('product__name')
        )

    @property
    def ordered_quantity(self):
        """ordered quantity."""
        return (
            self.obj.product.pricehistory_set.select_related().
            filter(orderhistory__quantity__gt=0).
            aggregate(Sum('orderhistory__quantity')).
            get('orderhistory__quantity__sum')
        )

    @property
    def received_quantity(self):
        """received quantity."""
        quantity = (
            self.obj.product.pricehistory_set.select_related().
            filter(orderhistory__receivehistory__quantity__gte=0).
            aggregate(Sum('orderhistory__receivehistory__quantity')).
            get('orderhistory__receivehistory__quantity__sum')
        )
        if quantity is None:
            quantity = 0
        return quantity

    @property
    def unpacked_quantity(self):
        """unpacked quantity."""
        quantity = (
            self.obj.product.unpackhistory_set.select_related().
            aggregate(Sum('quantity')).
            get('quantity__sum')
        )
        if quantity is None:
            quantity = 0
        return quantity

    @property
    def remain_quantity(self):
        """remain quantity."""
        if self.ordered_quantity >= self.received_quantity:
            return self.received_quantity - self.unpacked_quantity
        else:
            return 0
