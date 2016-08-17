# -*- coding: utf-8 -*-
"""backyard.inventory.models.product."""
from django.db import models

from . import BaseModel
from .maker import Maker


class Product(BaseModel):
    """Products."""
    name = models.CharField(unique=True, max_length=255)
    maker = models.ForeignKey(Maker)

    def __str__(self):
        return self.name
