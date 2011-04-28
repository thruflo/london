#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Provides a WSGI application factory entry point.
"""

from weblayer.component import registry
from weblayer.interfaces import IPathRouter
from weblayer.route import RegExpPathRouter

from weblayer import Bootstrapper, WSGIApplication

def factory(global_config, **local_conf):
    """
    """
    
    # merge the global and local config
    config = local_conf.copy()
    config.update(global_config)
    
    # make `config['template_directories']` a list
    config['template_directories'] = [config['template_directory_path']]
    
    # if rebuilding the db from scratch, first kill the existing data
    if config.has_key('bootstrap_db'):
        if config['db'] == 'sqlite':
            import os
            if os.path.exists(config['sqlite_path']):
                os.unlink(config['sqlite_path'])
        else:
            raise NotImplementedError
        
    # register the components aside from the ``path_router``, because
    # registering a ``path_router`` means importing ``model`` and importing
    # ``model`` requires a registered ``ISettings`` component already
    bootstrapper = Bootstrapper(settings=config)
    settings, path_router = bootstrapper(path_router=object())
    
    # now we can do stuff which imports model, starting by importing the
    # url mapping to use when registering a path router
    from urls import mapping
    path_router = RegExpPathRouter(mapping)
    registry.registerUtility(path_router, IPathRouter)
    
    # if rebuilding the db from scratch, now create the initial data
    if config.has_key('bootstrap_db'):
        import model
        model.bootstrap()
    
    # if requested, enter an interactive shell
    if config.has_key('shell'):
        import code
        code.interact()
    
    # return a wsgi app
    return WSGIApplication(settings, path_router)
    

