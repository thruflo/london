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
        r'/places/([0-9]*)/',
        Place
    ), (
        r'/options/',
        Options
    ), (
        r'/nolocation/',
        NoLocation
    )
]
