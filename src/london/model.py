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

special_character = re.compile(r'[^a-z0-9]', re.U | re.I)

from os.path import dirname, join as join_path

from sqlalchemy import create_engine, desc, func
from sqlalchemy import Table, Column, MetaData, ForeignKey
from sqlalchemy import BigInteger, Boolean, Date, Float, Integer, LargeBinary 
from sqlalchemy import PickleType, Unicode, UnicodeText
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker, relation, synonym
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import asc

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
    description = Column(UnicodeText, nullable=False)
    
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    image = Column(LargeBinary, nullable=False)
    address = Column(UnicodeText, nullable=False)
    url = Column(Unicode)
    
    google_place_reference = Column(Unicode, nullable=False, unique=True)
    foursquare_venue_id = Column(Unicode, nullable=False, unique=True)
    facebook_graph_id = Column(Unicode, nullable=False, unique=True)
    
    viewed = relation("User", secondary=places_users_viewed)
    bookmarked = relation("User", secondary=places_users_bookmarked)
    
    categories = relation("Category", secondary=places_categories)
    tags = relation("Tag", secondary=places_tags)
    
    def __repr__(self):
        return '<place title="%s">' % self.title
        
    
    
    def bookmark(self, user, should_commit=True):
        if not user in self.bookmarked:
            if should_commit:
                db.begin()
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
            if should_commit:
                db.begin()
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
            if should_commit:
                db.begin()
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
        
    
    
    @classmethod
    def get_by_category(cls, value, ll):
        """
        """
        
        query = db.query(cls).join('categories').filter(Category.value==value)
        
        # if we have a location, sort by nearest to the user
        if ll is not None:
            parts = ll.split('%2C')
            latitude = parts[0]
            longitude = parts[1]
            query = query.order_by(
                asc(
                    func.abs(Place.latitude - latitude) +
                    func.abs(Place.longitude - longitude)
                )
            )
        else: # otherwise sort by title
            query.order_by(Place.title)
        
        return query.all()
        
    
    


class Category(SQLModel):
    """
    """
    
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, nullable=False)
    
    value = Column(Unicode, unique=True)
    label = Column(Unicode)
    
    sort_order = Column(Integer, nullable=False)
    
    places = relation("Place", secondary=places_categories)
    
    @classmethod
    def get_all(cls):
        query = db.query(cls).order_by(cls.sort_order)
        return query.all()
        
    
    
    @classmethod
    def get_by_value(cls, value):
        if not isinstance(value, unicode):
            value = unicode(value)
        query = db.query(cls).filter_by(value=value)
        return query.first()
        
    
    
    def __repr__(self):
        return '<category value="%s">' % self.value
        
    
    

class Tag(SQLModel):
    """
    """
    
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, nullable=False)
    
    value = Column(Unicode, unique=True)
    label = Column(Unicode)
    
    places = relation("Place", secondary=places_tags)
    
    @classmethod
    def get_by_value(cls, value):
        if not isinstance(value, unicode):
            value = unicode(value)
        query = db.query(cls).filter_by(value=value)
        return query.one()
        
    
    
    def __repr__(self):
        return '<tag value="%s">' % self.value
        
    
    


def db_factory(settings):
    """
    """
    
    import logging
    logging.info(settings)
    
    # use sqlite in development
    if settings['dev_mode']: 
        sqlite_path = 'sqlite:///%s' % os.path.abspath(settings['sqlite_path'])
        engine = create_engine(sqlite_path, echo=False)
    else: # use postgresql in production
        raise NotImplementedError
    SQLModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autocommit=True)
    session = Session()
    return session
    

def bootstrap(session):
    """ Populate the database.
    """
    
    session.begin()
    
    # create categories
    i = 0
    labels = (
        u'Coffee',
        u'Snack',
        u'Meal',
        u'Drink'
    )
    for item in labels:
        value = special_character.sub('_', item.lower())
        category = Category(value=value, label=item, sort_order=i)
        session.add(category)
    
    # parse places
    
    from glob import glob
    from yaml import load, Loader
    
    here = os.path.dirname(__file__)
    data_directory_path = os.path.join(here, 'static', 'data')
    directories = glob(os.path.join(data_directory_path, '*'))
    
    for path in directories:
        
        index_file = open(os.path.join(path, 'index.yaml'))
        data = load(index_file, Loader=Loader)
        index_file.close()
        
        image_file = open(os.path.join(path, 'thumbnail.jpg'), 'rb')
        image_data = image_file.read()
        image_file.close()
        
        place = Place(
            title = data['title'],
            description = data['description'],
            latitude = float(data['latitude']),
            longitude = float(data['longitude']),
            image = image_data,
            address = data['address'],
            url = data['url'],
            google_place_reference = data['google_place_reference'],
            foursquare_venue_id = data['foursquare_venue_id'],
            facebook_graph_id = data['facebook_graph_id']
        )
        
        for value in data['categories']:
            category = Category.get_by_value(value)
            if category not in place.categories:
                place.categories.append(category)
        
        for value in data['tags']:
            try:
                tag = Tag.get_by_value(value)
            except NoResultFound:
                tag = Tag(value=value, label=value)
                session.add(tag)
            if tag not in place.tags:
                place.tags.append(tag)
            
        session.add(place)
        
    # commit changes
    try:
        session.commit()
    except IntegrityError, err:
        logging.error(err)
        session.rollback()
    

