# -*- coding: utf-8 -*-
"""backyard.inventory.models.shop."""
from django.db import models

from . import BaseModel


class Shop(BaseModel):
    """External Shop."""
    name = models.CharField(unique=True, max_length=255)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name
