# -*- coding: utf-8 -*-
"""backyard.inventory.queryset.order_history."""


class OrderQuerySet(object):
    """Order quereis."""

    def __init__(self, obj):
        """initialize."""
        self.obj = obj

    def ordered_product(self):
        """ordered product."""
        return self.obj.order_item.product

    def product_price(self):
        """product price."""
        return self.obj.order_item.price

    def amount(self):
        """amount query."""
        return self.obj.order_item.price * self.obj.quantity
