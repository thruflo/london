#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
"""

__all__ = [
    'Location'
]

class Location(object):
    """ Encapsulates a point on a map.
    """
    
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        
    
    def validate(self):
        """ Raises ``ValueError`` if lat or lon are invalid.
        """
        
        float(self.latitude)
        float(self.longitude)
        
    
    

