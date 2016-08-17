# -*- coding: utf-8 -*-
"""backyard.inventory.models.receive_history."""
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _

from . import OwnerHistory
from .order_history import OrderHistory


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
