#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
"""

from weblayer import RequestHandler

class RelayToTemplate(RequestHandler):
    """
    """
    
    def get(self, name='listings'):
        
        return self.render('%s.tmpl' % name)
        
    
    

