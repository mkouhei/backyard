# -*- coding: utf-8 -*-
"""backyard.inventory.models.external_account."""
from django.db import models

from . import OwnerModel
from .shop import Shop


class ExternalAccount(OwnerModel):
    """Online shop account."""
    name = models.CharField(unique=True, max_length=255)
    encrypted_password = models.CharField(max_length=255)
    email = models.EmailField()
    shop = models.ForeignKey(Shop)

    class Meta(object):
        """meta data."""
        unique_together = ('name', 'shop')

    def __str__(self):
        return self.name
