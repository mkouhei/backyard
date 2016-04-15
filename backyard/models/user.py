# -*- coding: utf-8 -*-
"""backyard.models.user."""
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from .base import Base


class User(Base):
    """User model."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    email = Column(Text, unique=True)
    encrypted_password = Column(Text, nullable=True)

Index('user', User.name, unique=True, mysql_length=255)
