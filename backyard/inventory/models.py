# -*- coding: utf-8 -*-
"""backyard.inventory.models."""
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group


class BaseModel(models.Model):
    """Abstract base model."""
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User)
    group = models.ForeignKey(Group)

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


class ReceiveHistory(BaseHistory):
    """Receive histories."""
    received_at = models.DateTimeField(auto_now=True)
    received_item = models.ForeignKey(OrderHistory)
    quantity = models.IntegerField()

    class Meta(object):
        """Meta data."""
        unique_together = ('received_item', 'received_at')

    def __str__(self):
        return '{0}'.format(self.received_item)


def received_receiver(sender, instance, created, **kwargs):
    """unreceived item."""
    ReceiveHistory(received_item=instance, quantity=0).save()
post_save.connect(received_receiver, sender=OrderHistory)


class UnpackHistory(BaseHistory):
    """Unpack histories."""
    unpacked_at = models.DateTimeField(auto_now=True)
    unpacked_item = models.ForeignKey(Product)
    quantity = models.IntegerField()

    def __str__(self):
        return self.unpacked_item.name


def unpacked_receiver(sender, instance, created, **kwargs):
    """unpack item."""
    UnpackHistory(unpacked_item=instance,
                  quantity=0).save()
post_save.connect(unpacked_receiver, sender=Product)


class Inventory(BaseModel):
    """Inventory."""
    product = models.ForeignKey(Product)


def inventory_receiver(sender, instance, created, **kwargs):
    """inventory item."""
    Inventory(product=instance).save()
post_save.connect(inventory_receiver, sender=Product)
