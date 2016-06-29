# -*- coding: utf-8 -*-
"""backyard.inventory.models."""
from django.db import models


class BaseModel(models.Model):
    """Abstract base model."""
    id = models.AutoField(primary_key=True)

    class Meta(object):
        """meta class."""
        abstract = True


class BaseHistory(BaseModel):
    """Abstract History base model."""
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        """meta class."""
        abstract = True


class Maker(BaseModel):
    """Maker."""
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name


class Product(BaseModel):
    """Products."""
    name = models.CharField(unique=True, max_length=255)
    maker = models.ForeignKey(Maker)

    def __str__(self):
        return self.name


class ExternalAccount(BaseModel):
    """Online shop account."""
    name = models.CharField(max_length=255)
    encrypted_password = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Shop(BaseModel):
    """External Shop."""
    name = models.CharField(unique=True, max_length=255)
    url = models.URLField(unique=True)
    user = models.ForeignKey(ExternalAccount)

    def __str__(self):
        return self.name


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


class OrderHistory(BaseHistory):
    """Order histories."""
    ordered_at = models.DateTimeField()
    order_item = models.ForeignKey(PriceHistory)
    count = models.IntegerField()

    class Meta(object):
        """Meta data."""
        unique_together = ('order_item', 'ordered_at')

    def __str__(self):
        return '{0} * {1} ({2})'.format(self.order_item,
                                        self.count,
                                        self.ordered_at)

    def amount(self):
        """amount."""
        return self.order_item.price * self.count


class ReceiveHistory(BaseHistory):
    """Receive histories."""
    received_at = models.DateTimeField()
    received_item = models.ForeignKey(OrderHistory)
    difference_count = models.IntegerField(default=0)

    class Meta(object):
        """Meta data."""
        unique_together = ('received_item', 'received_at')

    def __str__(self):
        return '{0}'.format(self.received_item)


class UnpackHistory(BaseHistory):
    """Unpack histories."""
    unpacked_at = models.DateTimeField()
    unpacked_item = models.ForeignKey(Product)
    count = models.IntegerField()


class Inventory(BaseModel):
    """Inventory."""
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
