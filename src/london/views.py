#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
"""

from weblayer import RequestHandler

class RelayToTemplate(RequestHandler):
    """
    """
    
    def get(self, name):
        
        import logging
        logging.info(name)
        
        return self.render('%s.tmpl' % name)
        
    
    

