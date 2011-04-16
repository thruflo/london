#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
"""

from weblayer import Bootstrapper, WSGIApplication
from urls import mapping

def factory(global_config, **local_conf):
    """
    """
    
    # merge the global and local config
    config = global_config
    config.update(local_conf)
    
    # make `config['template_directories']` a list
    config['template_directories'] = [config['template_directory_path']]
    
    # instantiate the bootstrapper
    bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
    
    # return a bootstrapped `WSGIApplication`
    return WSGIApplication(*bootstrapper())
    

