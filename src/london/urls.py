#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
"""

from views import RelayToTemplate

mapping = [(
        r'/(.*)\/',
        RelayToTemplate
    ), (
        r'/',
        RelayToTemplate
    )
]
