# -*- coding: utf-8 -*-
"""backyard.inventory.models.inventory."""
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save

from . import OwnerModel
from .product import Product
from .order_history import OrderHistory


class Inventory(OwnerModel):
    """Inventory."""
    product = models.ForeignKey(Product)


def inventory_receiver(sender, instance, created, **kwargs):
    """inventory item."""
    try:
        Inventory.objects.get(
            Q(product=instance.ordered_item.product) &
            Q(owner=instance.owner) &
            Q(group=instance.group)
        )
    except Inventory.DoesNotExist:
        Inventory(product=instance.ordered_item.product,
                  owner=instance.owner,
                  group=instance.group).save()
post_save.connect(inventory_receiver, sender=OrderHistory)
