# -*- coding: utf-8 -*-
"""backyard.inventory.models.maker."""
from django.db import models

from . import BaseModel


class Maker(BaseModel):
    """Maker."""
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name
