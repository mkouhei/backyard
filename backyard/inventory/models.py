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


class ExtenalAccount(BaseModel):
    """Online shop account."""
    name = models.CharField(max_length=255)
    encrypted_password = models.CharField(max_length=255)
    email = models.EmailField()


class Shop(BaseModel):
    """External Shop."""
    name = models.CharField(unique=True, max_length=255)
    url = models.URLField(unique=True)
    user = models.ForeignKey(ECUser)


class Inventory(BaseModel):
    """Inventory."""
    production = models.ForeignKey(Production)
    amount = models.IntegerField()
