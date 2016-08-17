# -*- coding: utf-8 -*-
"""backyard.inventory.models.unpack_history."""
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, Sum
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _

from . import OwnerHistory
from .product import Product
from .receive_history import ReceiveHistory


class UnpackHistory(OwnerHistory):
    """Unpack histories."""
    unpacked_at = models.DateTimeField(auto_now=True)
    unpacked_item = models.ForeignKey(Product)
    quantity = models.IntegerField()

    def __init__(self, *args, **kwargs):
        super(UnpackHistory, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.unpacked_item.name


def validate_unpack_quantity(sender, instance, **kwargs):
    """validate unpacke quantity."""
    received = ReceiveHistory.objects.filter(
        Q(received_item__ordered_item__product=instance.unpacked_item)
    ).aggregate(Sum('quantity')).get('quantity__sum')
    unpacked = UnpackHistory.objects.filter(
        Q(unpacked_item=instance.unpacked_item)
    ).aggregate(Sum('quantity')).get('quantity__sum')
    if unpacked is None:
        unpacked = 0
    remain = received - unpacked
    if instance.quantity > remain:
        raise ValidationError(
            _('%(unpack)s is not over than remain %(remain)s'),
            params={'unpack': instance.quantity,
                    'remain': remain}
        )
pre_save.connect(validate_unpack_quantity, sender=UnpackHistory)
