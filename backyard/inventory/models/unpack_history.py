# -*- coding: utf-8 -*-
"""backyard.inventory.models.unpack_history."""
from django.db import models

from . import OwnerHistory
from .product import Product


class UnpackHistory(OwnerHistory):
    """Unpack histories."""
    unpacked_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()

    class Meta(object):
        """Meta data."""
        unique_together = ('product', 'unpacked_at', 'owner')

    def __init__(self, *args, **kwargs):
        super(UnpackHistory, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.product.name
