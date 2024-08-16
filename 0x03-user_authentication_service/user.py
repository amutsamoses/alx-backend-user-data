#!/usr/bin/env python3

"""
creating a User model definition using SQLAlchemy
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    sqlalchemy model for users table
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    session_id = Column(String(255), nullable=True)
    reset_token = Column(String(255), nullable=True)
