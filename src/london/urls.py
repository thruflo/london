#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
"""

from views import *

mapping = [(
        r'/',
        Index
    ), (
        r'/categories/(\w*)/',
        Category
    ), (
        r'/categories/(\w*)/map/',
        CategoryMap
    ), (
        r'/places/(\w*)/',
        Place
    ), (
        r'/options/',
        Options
    ), (
        r'/nolocation/',
        NoLocation
    )
]
