#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
"""

__all__ = [
    'Index',
    'Category',
    'CategoryMap',
    'Place',
    'Options',
    'NoLocation'
]

import model

from utils import Location
from weblayer import RequestHandler

class Index(RequestHandler):
    """ List of categories.
    """
    
    def get(self):
        categories = model.Category.get_all()
        return self.render('index.tmpl', categories=categories)
        
    
    


class LocationMixin(object):
    """ Provides ``self.location``.
    """
    
    @property
    def location(self):
        """
        """
        
        if not hasattr(self, '_location'):
            self._location = None
            ll = self.request.cookies.get('ll', None)
            if ll is not None:
                parts = ll.split('%2C')
                location = Location(parts[0], parts[1])
                location.validate()
                self._location = location
            
        return self._location
        
    
    


class Category(RequestHandler, LocationMixin):
    """ List of places in a category, nearest first.
    """
    
    def get(self, value):
        """
        """
        
        category = model.Category.get_by_value(value)
        places = model.Place.get_by_category(value, self.location)
        
        return self.render('category.tmpl', category=category, places=places)
        
    
    

class CategoryMap(RequestHandler, LocationMixin):
    """ Places in a category on a google map.
    """
    
    def get(self, value):
        """
        """
        
        category = model.Category.get_by_value(value)
        places = model.Place.get_by_category(value, self.location)
        
        return self.render('categorymap.tmpl', category=category, places=places)
        
    
    


class Place(RequestHandler):
    """ Information about a specific place.
    """
    
    def get(self, id):
        """
        """
        
        raise NotImplementedError
        
    
    


class Options(RequestHandler):
    """ Dialog providing configuration options.
    """
    
    def get(self):
        """
        """
        
        return self.render('options.tmpl')
        
    
    

class NoLocation(RequestHandler):
    """ Dialog informing user location not known.
    """
    
    def get(self):
        return self.render('nolocation.tmpl')
        
    
    

