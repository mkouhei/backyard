# -*- coding: utf-8 -*-
"""backyard.inventory.models."""
from django.db import models
from django.db.models import Q, Sum


class BaseModel(models.Model):
    """Abstract base model."""
    id = models.AutoField(primary_key=True)

    class Meta(object):
        """meta class."""
        abstract = True


class BaseHistory(BaseModel):
    """Abstract History base model."""
    created_at = models.DateTimeField(auto_now=True)

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
    quantity = models.IntegerField()

    class Meta(object):
        """Meta data."""
        unique_together = ('order_item', 'ordered_at')

    def __str__(self):
        return '{0} * {1} ({2})'.format(self.order_item,
                                        self.quantity,
                                        self.ordered_at)

    def amount(self):
        """amount."""
        return self.order_item.price * self.quantity


class ReceiveHistory(BaseHistory):
    """Receive histories."""
    received_at = models.DateTimeField()
    received_item = models.ForeignKey(OrderHistory)
    difference_quantity = models.IntegerField(default=0)

    class Meta(object):
        """Meta data."""
        unique_together = ('received_item', 'received_at')

    def __str__(self):
        return '{0}'.format(self.received_item)


class UnpackHistory(BaseHistory):
    """Unpack histories."""
    unpacked_at = models.DateTimeField()
    unpacked_item = models.ForeignKey(Product)
    quantity = models.IntegerField()

    def __str__(self):
        return self.unpacked_item.name


class Inventory(BaseModel):
    """Inventory."""
    product = models.ForeignKey(Product)

    def quantity(self):
        """quantity."""
        # select sum(quantity) from inventory_orderhistory
        # where order_item_id = 1;
        ordered_quantity = OrderHistory.objects.filter(
            Q(order_item__product=self.product)).aggregate(Sum('quantity'))

        # select sum(r.difference_quantity)
        # from inventory_receivehistory as r
        # inner join inventory_orderhistory as o
        # on (r.received_item_id = o.id) where o.order_item_id = 1;
        ordered_item = OrderHistory.objects.filter(
            Q(order_item__product=self.product)
        ).values('order_item__product').distinct()
        received_item = ReceiveHistory.objects.filter(
            Q(received_item=ordered_item)
        ).aggregate(Sum('difference_quantity'))

        # select sum(quantity) from inventory_unpackhistory
        # where unpacked_item_id = 1;
        unpacked_quantity = UnpackHistory.objects.filter(
            Q(unpacked_item=self.product)).aggregate(Sum('quantity'))
        return (ordered_quantity.get('quantity__sum') +
                received_item.get('difference_quantity__sum') -
                unpacked_quantity.get('quantity__sum'))
