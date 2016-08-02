# -*- coding: utf-8 -*-
"""backyard.inventory.queryset.order_history."""


class OrderQuerySet(object):
    """Order quereis."""

    def __init__(self, obj):
        """initialize."""
        self.obj = obj

    @property
    def ordered_product(self):
        """ordered product."""
        return self.obj.ordered_item.product

    @property
    def product_price(self):
        """product price."""
        return self.obj.ordered_item.price

    @property
    def amount(self):
        """amount query."""
        return self.obj.ordered_item.price * self.obj.quantity
