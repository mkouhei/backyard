# -*- coding: utf-8 -*-
"""backyard.inventory.models.price_history."""
from django.db import models

from . import BaseHistory
from .product import Product
from .shop import Shop


class PriceHistory(BaseHistory):
    """Price histories."""
    CURRENCY_UNIT = (
        ('JPY', 'JPY'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )
    product = models.ForeignKey(Product)
    shop = models.ForeignKey(Shop)
    registered_date = models.DateField()
    price = models.IntegerField()
    currency_unit = models.CharField(max_length=10,
                                     choices=CURRENCY_UNIT,
                                     default='JPY')

    class Meta(object):
        """Meta data."""
        unique_together = ('product', 'registered_date')

    def __str__(self):
        return '{0} {1}'.format(self.product, self.price)
