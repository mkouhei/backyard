# -*- coding: utf-8 -*-
"""backyard.models."""
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    email = Column(Text, unique=True)
    encrypted_password = Column(Text, nullable=True)

Index('user', User.name, unique=True, mysql_length=255)
