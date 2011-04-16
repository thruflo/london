#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""We use SQLAlchemy_ in declarative_ mode.
  
  .. _SQLAlchemy: http://www.sqlalchemy.org/
  .. _declarative: http://www.sqlalchemy.org/docs/reference/ext/declarative.html
"""

import datetime
import logging
import math
import os
import sys
import re

from os.path import dirname, join as join_path

from sqlalchemy import create_engine, desc, func
from sqlalchemy import Table, Column, MetaData, ForeignKey
from sqlalchemy import Boolean, Date, Integer, PickleType, Unicode, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker, relation, synonym

SQLModel = declarative_base()

places_categories = Table(
    'places_categories',
    SQLModel.metadata,
    Column('place_id', Integer, ForeignKey('places.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)
places_tags = Table(
    'places_tags',
    SQLModel.metadata,
    Column('place_id', Integer, ForeignKey('places.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)
places_users_viewed = Table(
    'places_users_viewed',
    SQLModel.metadata,
    Column('place_id', Integer, ForeignKey('places.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)
places_users_bookmarked = Table(
    'places_users_bookmarked',
    SQLModel.metadata,
    Column('place_id', Integer, ForeignKey('places.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class User(SQLModel):
    """
    """
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Unicode)
    username = Column(Unicode, unique=True)
    password = Column(Unicode)
    email_address = Column(Unicode, unique=True)
    is_admin = Column(Boolean, default=False)
    viewed = relation("Place", secondary=places_users_viewed)
    bookmarked = relation("Place", secondary=places_users_bookmarked)
    
    def __repr__(self):
        return '<user username="%s">' % self.username
        
    
    
    @classmethod
    def authenticate(cls, username, password):
        query = db.query(cls).filter_by(username=username, password=password)
        return query.first()
        
    
    
    @classmethod
    def get_all(cls):
        query = db.query(cls).order_by(cls.username)
        return query.all()
        
    
    
    @classmethod
    def get_by_username(cls, username):
        if not isinstance(username, unicode):
            username = unicode(username)
        query = db.query(cls).filter_by(username=username)
        return query.one()
        
    
    

class Place(SQLModel):
    """
    """
    
    __tablename__ = 'places'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(Unicode, nullable=False, unique=True)
    description = Column(UnicodeText)
    viewed = relation("User", secondary=places_users_viewed)
    bookmarked = relation("User", secondary=places_users_bookmarked)
    categories = relation("Category", secondary=places_categories)
    tags = relation("Tag", secondary=places_tags)
    
    def __repr__(self):
        return '<place title="%s">' % self.title
        
    
    
    def bookmark(self, user, should_commit=True):
        if not user in self.bookmarked:
            self.bookmarked.append(user)
            db.add(self)
            if should_commit:
                try:
                    db.commit()
                except IntegrityError, err:
                    logging.err(err)
                    db.rollback()
        
        
    
    def unbookmark(self, user, should_commit=True):
        if user in self.bookmarked:
            self.bookmarked.remove(user)
            db.add(self)
            if should_commit:
                try:
                    db.commit()
                except IntegrityError, err:
                    logging.err(err)
                    db.rollback()
        
    
    def mark_viewed(self, user, should_commit=True):
        if not user in self.viewed:
            self.viewed.append(user)
            db.add(self)
            if should_commit:
                try:
                    db.commit()
                except IntegrityError, err:
                    logging.err(err)
                    db.rollback()
        
        
    
    
    def viewed_by(self, user):
        return user in self.viewed
        
    
    def bookmarked_by(self, user):
        return user in self.bookmarked
        
    
    

class Category(SQLModel):
    """
    """
    
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, nullable=False)
    value = Column(Unicode, unique=True)
    places = relation("Place", secondary=places_categories)
    
    def __repr__(self):
        return '<category value="%s">' % self.value
        
    
    

class Tag(SQLModel):
    """
    """
    
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, nullable=False)
    value = Column(Unicode, unique=True)
    places = relation("Place", secondary=places_tags)
    
    def __repr__(self):
        return '<tag value="%s">' % self.value
        
    
    


def db_factory(settings):
    """
    """
    
    # use sqlite in development
    if settings['dev_mode']: 
        sqlite_path = 'sqlite:///%s' % os.path.abspath(settings['sqlite_path'])
        engine = create_engine(sqlite_path, echo=False)
    else: # use postgresql in production
        raise NotImplementedError
    SQLModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
    

