# -*- coding: utf-8 -*-
"""backyard.inventory.models.order_history."""
from django.db import models

from . import OwnerHistory
from .product import Product
from .price_history import PriceHistory


class OrderHistory(OwnerHistory):
    """Order histories."""
    product = models.ForeignKey(Product)
    price = models.ForeignKey(PriceHistory)
    ordered_at = models.DateTimeField(auto_now=True)
    ordered_quantity = models.IntegerField()
    received_at = models.DateTimeField(null=True)
    received_quantity = models.IntegerField(default=0)

    class Meta(object):
        """Meta data."""
        unique_together = ('product', 'ordered_at', 'owner')

    def __str__(self):
        return '{0} * {1} ({2})'.format(self.product,
                                        self.ordered_quantity,
                                        self.ordered_at)
        
