# -*- coding: utf-8 -*-
"""backyard.inventory.models."""
from django.contrib.auth.models import User, Group
from django.db import models


class BaseModel(models.Model):
    """Abstract base model."""
    id = models.AutoField(primary_key=True)

    class Meta(object):
        """meta class."""
        abstract = True


class OwnerModel(BaseModel):
    """Abstract owner model."""
    owner = models.ForeignKey(User)
    group = models.ForeignKey(Group)

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


class OwnerHistory(OwnerModel):
    """Abstract History base model."""
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        """meta class."""
        abstract = True
