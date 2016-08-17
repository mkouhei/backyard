# -*- coding: utf-8 -*-
"""backyard.inventory.models.order_history."""
from django.db import models

from . import OwnerHistory
from .price_history import PriceHistory


class OrderHistory(OwnerHistory):
    """Order histories."""
    ordered_at = models.DateTimeField(auto_now=True)
    ordered_item = models.ForeignKey(PriceHistory)
    quantity = models.IntegerField()

    class Meta(object):
        """Meta data."""
        unique_together = ('ordered_item', 'ordered_at')

    def __str__(self):
        return '{0} * {1} ({2})'.format(self.ordered_item,
                                        self.quantity,
                                        self.ordered_at)
