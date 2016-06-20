# -*- coding: utf-8 -*-
"""backyard.inventory.models."""
from django.db import models


class BaseModel(models.Model):
    """Abstract base model."""
    id = models.AutoField(primary_key=True)

    class Meta(object):
        """meta class."""
        abstract = True


class Maker(BaseModel):
    """Maker."""
    name = models.CharField(unique=True, max_length=255)


class Production(BaseModel):
    """Productions."""
    name = models.CharField(unique=True, max_length=255)
    maker = models.ForeignKey(Maker)


class Inventory(BaseModel):
    """Inventory."""
    production = models.ForeignKey(Production)
    amount = models.IntegerField()
