# -*- coding: utf-8 -*-
"""backyard.inventory.models."""
from django.db import models


class BaseModel(models.Model):
    """Abstract base model."""
    id = models.AutoField(primary_key=True)

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


class Product(BaseModel):
    """Products."""
    name = models.CharField(unique=True, max_length=255)
    maker = models.ForeignKey(Maker)


class ExternalAccount(BaseModel):
    """Online shop account."""
    name = models.CharField(max_length=255)
    encrypted_password = models.CharField(max_length=255)
    email = models.EmailField()


class Shop(BaseModel):
    """External Shop."""
    name = models.CharField(unique=True, max_length=255)
    url = models.URLField(unique=True)
    user = models.ForeignKey(ExternalAccount)


class PriceHistory(BaseHistory):
    """Price histories."""
    product = models.ForeignKey(Product)
    shop = models.ForeignKey(Shop)
    registred_date = models.DateField()
    price = models.IntegerField()


class Inventory(BaseModel):
    """Inventory."""
    product = models.ForeignKey(Product)
    amount = models.IntegerField()


class OrderHistory(BaseHistory):
    """Order histories."""
    ordered_at = models.DateTimeField()
    order_item = models.ForeignKey(Product)
    price = models.ForeignKey(PriceHistory)
    count = models.IntegerField()
    amount = models.IntegerField()
