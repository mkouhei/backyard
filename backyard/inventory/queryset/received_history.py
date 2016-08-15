# -*- coding: utf-8 -*-
"""backyard.inventory.queryset.received_history."""


class ReceivedQuerySet(object):
    """Received queries."""

    def __init__(self, obj):
        """initialize."""
        self.obj = obj

    @property
    def product_name(self):
        """product name."""
        return self.ordered_product.name

    @property
    def ordered_product(self):
        """ordered product."""
        return self.obj.received_item.ordered_item.product

    @property
    def ordered_quantity(self):
        """ordered quantity."""
        return self.obj.received_item.ordered_item.quantity
