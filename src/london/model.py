#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""We use SQLAlchemy_ in declarative_ mode.
  
  Note that there *must* be a ``weblayer.interfaces.ISettings`` instance
  registered before importing this module.
  
  .. _SQLAlchemy: http://www.sqlalchemy.org/
  .. _declarative: http://www.sqlalchemy.org/docs/reference/ext/declarative.html
"""

import logging
import re
special_character = re.compile(r'[^a-z0-9]', re.U | re.I)

from os.path import abspath, dirname, join as join_path

from sqlalchemy import create_engine, desc, func
from sqlalchemy import Table, Column, MetaData, ForeignKey
from sqlalchemy import BigInteger, Boolean, Date, Float, Integer, LargeBinary 
from sqlalchemy import PickleType, Unicode, UnicodeText
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relation, scoped_session, sessionmaker, synonym
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.pool import NullPool
from sqlalchemy.sql.expression import asc

def engine_factory():
    """ Creates the engine specified by the application settings.
    """
    
    from weblayer.interfaces import ISettings
    from weblayer.component import registry
    
    settings = registry.getUtility(ISettings)
    
    if settings.get('db') == 'sqlite':
        sqlite_path = 'sqlite:///%s' % abspath(settings['sqlite_path'])
        return create_engine(sqlite_path, poolclass=NullPool, echo=False)
    else: 
        raise NotImplementedError
    

engine = engine_factory()

Session = scoped_session(sessionmaker(bind=engine))
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
places_users_favourites = Table(
    'places_users_favourites',
    SQLModel.metadata,
    Column('place_id', Integer, ForeignKey('places.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class QueryMixin(object):
    """
    """
    
    query = Session.query_property()
    
    @classmethod
    def get_by_id(cls, id):
        """
        """
        
        return cls.query.get(id)
        
    
    


class User(SQLModel, QueryMixin):
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
    favourites = relation("Place", secondary=places_users_favourites)
    
    def __repr__(self):
        return '<user username="%s">' % self.username
        
    
    
    @classmethod
    def authenticate(cls, username, password):
        query = Session().query(cls).filter_by(username=username, password=password)
        return query.first()
        
    
    
    @classmethod
    def get_all(cls):
        query = Session().query(cls).order_by(cls.username)
        return query.all()
        
    
    
    @classmethod
    def get_by_username(cls, username):
        if not isinstance(username, unicode):
            username = unicode(username)
        query = Session().query(cls).filter_by(username=username)
        return query.one()
        
    
    

class Place(SQLModel, QueryMixin):
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
    favourites = relation("User", secondary=places_users_favourites)
    
    categories = relation("Category", secondary=places_categories)
    tags = relation("Tag", secondary=places_tags)
    
    def __repr__(self):
        return '<place title="%s">' % self.title
        
    
    
    def favourite(self, user, should_commit=True):
        session = Session()
        if not user in self.favourites:
            if should_commit:
                session.begin()
            self.favourites.append(user)
            session.add(self)
            if should_commit:
                try:
                    session.commit()
                except IntegrityError, err:
                    logging.err(err)
                    session.rollback()
                
            
        
    
    def unfavourite(self, user, should_commit=True):
        session = Session()
        if user in self.favourites:
            if should_commit:
                session.begin()
            self.favourites.remove(user)
            session.add(self)
            if should_commit:
                try:
                    session.commit()
                except IntegrityError, err:
                    logging.err(err)
                    session.rollback()
                
            
        
    
    def mark_viewed(self, user, should_commit=True):
        session = Session()
        if not user in self.viewed:
            if should_commit:
                session.begin()
            self.viewed.append(user)
            session.add(self)
            if should_commit:
                try:
                    session.commit()
                except IntegrityError, err:
                    logging.err(err)
                    session.rollback()
        
        
    
    
    def viewed_by(self, user):
        return user in self.viewed
        
    
    def favourites_by(self, user):
        return user in self.favourites
        
    
    
    @classmethod
    def get_by_category(cls, value, location=None):
        """
        """
        
        query = cls.query.join('categories').filter(Category.value==value)
        
        # if we have a location, sort by nearest to the user
        if location is not None:
            query = query.order_by(
                asc(
                    func.abs(Place.latitude - location.latitude) +
                    func.abs(Place.longitude - location.longitude)
                )
            )
        else: # otherwise sort by title
            query.order_by(Place.title)
        
        return query.all()
        
    
    

class Category(SQLModel, QueryMixin):
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
        query = Session().query(cls).order_by(cls.sort_order)
        return query.all()
        
    
    
    @classmethod
    def get_by_value(cls, value):
        if not isinstance(value, unicode):
            value = unicode(value)
        query = Session().query(cls).filter_by(value=value)
        return query.first()
        
    
    
    def __repr__(self):
        return '<category value="%s">' % self.value
        
    
    

class Tag(SQLModel, QueryMixin):
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
        query = Session().query(cls).filter_by(value=value)
        return query.one()
        
    
    
    def __repr__(self):
        return '<tag value="%s">' % self.value
        
    
    


SQLModel.metadata.create_all(engine)

def bootstrap():
    """ Populate the database from scratch.
    """
    
    session = Session()
    
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
    
    here = dirname(__file__)
    data_directory_path = join_path(here, 'static', 'data')
    directories = glob(join_path(data_directory_path, '*'))
    
    for path in directories:
        
        index_file = open(join_path(path, 'index.yaml'))
        data = load(index_file, Loader=Loader)
        index_file.close()
        
        image_file = open(join_path(path, 'thumbnail.jpg'), 'rb')
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
    

