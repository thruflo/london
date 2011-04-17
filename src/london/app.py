#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
"""

from weblayer import Bootstrapper, WSGIApplication

def factory(global_config, **local_conf):
    """
    """
    
    # merge the global and local config
    config = local_conf.copy()
    config.update(global_config)
    
    # make `config['template_directories']` a list
    config['template_directories'] = [config['template_directory_path']]
    
    if config.get('dev_mode', False) and config.get('bootstrap_db', False):
        import os
        if os.path.exists(config['sqlite_path']):
            os.unlink()
        
    # create the db session
    import model
    model.db = model.db_factory(config)
    
    if config.get('dev_mode', False) and config.get('bootstrap_db', False):
        model.bootstrap(model.db)
    
    # instantiate the bootstrapper
    from urls import mapping
    bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
    
    # return a bootstrapped `WSGIApplication`
    return WSGIApplication(*bootstrapper())
    

