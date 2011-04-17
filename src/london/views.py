#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
"""

__all__ = [
    'Listings',
    'CategoryListing',
    
    'RelayToTemplate'
]

from weblayer import RequestHandler

import model

class Listings(RequestHandler):
    """
    """
    
    def get(self):
        categories = model.Category.get_all()
        return self.render('listings.tmpl', categories=categories)
        
    
    


class CategoryListing(RequestHandler):
    """
    """
    
    def get(self, value):
        """
        """
        
        import logging
        logging.warning('validate user input')
        
        category = model.Category.get_by_value(value)
        
        ll = self.request.cookies.get('ll', None)
        places = model.Place.get_by_category(value, ll)
        
        return self.render('category.tmpl', category=category, places=places)
        
    
    


class RelayToTemplate(RequestHandler):
    """
    """
    
    def get(self, name='listings'):
        
        return self.render('%s.tmpl' % name)
        
    
    

