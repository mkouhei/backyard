# -*- coding: utf-8 -*-
"""backyard.inventory.queryset.unpacked_history."""
from django.db.models import Q

from ..models.unpack_history import UnpackHistory


class UnpackQuerySet(object):
    """Unpack queries."""

    def __init__(self, product_id, group):
        """initialize."""
        self.product_id = product_id
        self.group = group
        self.unpack_query = UnpackHistory.objects.filter(
            Q(product__id=self.product_id) &
            Q(group=self.group)
        )

    @property
    def unpack(self):
        """unpacked."""
        return self.unpack_query.values(
            'unpacked_at',
            'quantity'
        )

    @property
    def product_name(self):
        """product name."""
        return self.unpack_query.values('product__name').first().get('product__name')
