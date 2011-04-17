#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
"""

from views import *

mapping = [
    
    (
        r'/categories/(\w*)/',
        CategoryListing
    ), 
    
    (
        r'/',
        Listings
    ),    
    
    
    
    
    (
        r'/(.*)\/',
        RelayToTemplate
    )
    
]
