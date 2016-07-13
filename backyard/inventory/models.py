# -*- coding: utf-8 -*-
"""backyard.inventory.models."""
from copy import copy
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, Sum
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    """Abstract base model."""
    id = models.AutoField(primary_key=True)

    class Meta(object):
        """meta class."""
        abstract = True


class OwnerModel(BaseModel):
    """Abstract owner model."""
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


class OwnerHistory(OwnerModel):
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


class Shop(BaseModel):
    """External Shop."""
    name = models.CharField(unique=True, max_length=255)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name


class ExternalAccount(OwnerModel):
    """Online shop account."""
    name = models.CharField(max_length=255)
    encrypted_password = models.CharField(max_length=255)
    email = models.EmailField()
    shop = models.ForeignKey(Shop)

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


class ReceiveHistory(OwnerHistory):
    """Receive histories."""
    received_at = models.DateTimeField(auto_now=True)
    received_item = models.ForeignKey(OrderHistory)
    quantity = models.IntegerField()

    class Meta(object):
        """Meta data."""
        unique_together = ('received_item', 'received_at')

    def __str__(self):
        return '{0}'.format(self.received_item)


def validate_receive_quantity(sender, instance, **kwargs):
    """validate receive quantity."""
    if instance.quantity > instance.received_item.quantity:
        raise ValidationError(
            _('%(received)s is not over than ordered %(ordered)s'),
            params={'received': instance.quantity,
                    'ordered': instance.received_item.quantity},
        )
pre_save.connect(validate_receive_quantity, sender=ReceiveHistory)


def received_receiver(sender, instance, created, **kwargs):
    """unreceived item."""
    ReceiveHistory(received_item=instance,
                   owner=instance.owner,
                   group=instance.group,
                   quantity=0).save()
post_save.connect(received_receiver, sender=OrderHistory)


class UnpackHistory(OwnerHistory):
    """Unpack histories."""
    unpacked_at = models.DateTimeField(auto_now=True)
    unpacked_item = models.ForeignKey(Product)
    quantity = models.IntegerField()

    def __init__(self, *args, **kwargs):
        super(UnpackHistory, self).__init__(*args, **kwargs)
        self.old = copy(self)

    def __str__(self):
        return self.unpacked_item.name


def validate_unpack_quantity(sender, instance, **kwargs):
    """validate unpacke quantity."""
    ordered = OrderHistory.objects.filter(
        Q(ordered_item__product=instance.unpacked_item)
    ).aggregate(Sum('quantity')).get('quantity__sum')
    received = ReceiveHistory.objects.filter(
        Q(received_item__ordered_item__product=instance.unpacked_item)
    ).aggregate(Sum('quantity')).get('quantity__sum')
    if ordered > received:
        remain = received - instance.old.quantity
    else:
        remain = 0
    if instance.quantity > remain:
        raise ValidationError(
            _('%(unpack)s is not over than remain %(remain)s'),
            params={'unpack': instance.quantity,
                    'remain': remain},
        )
pre_save.connect(validate_unpack_quantity, sender=UnpackHistory)


def unpacked_receiver(sender, instance, created, **kwargs):
    """unpack item."""
    UnpackHistory(unpacked_item=instance.ordered_item.product,
                  owner=instance.owner,
                  group=instance.group,
                  quantity=0).save()
post_save.connect(unpacked_receiver, sender=OrderHistory)


class Inventory(OwnerModel):
    """Inventory."""
    product = models.ForeignKey(Product)


def inventory_receiver(sender, instance, created, **kwargs):
    """inventory item."""
    Inventory(product=instance.ordered_item.product,
              owner=instance.owner,
              group=instance.group).save()
post_save.connect(inventory_receiver, sender=OrderHistory)
