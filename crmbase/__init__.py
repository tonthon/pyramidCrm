# -*- coding: utf-8 -*-
# * File Name : __init__.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 11-01-2012
# * Last Modified : mar. 20 mars 2012 12:09:20 CET
#
# * Project : crmbase
#
"""
    Pyramid main file used to launch our application
"""
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config

from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from crmbase.models import initialize_sql
from crmbase.security import build_avatar
from crmbase.security import RootFactory

def main(global_config, **settings):
    """
        Main function : returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    auth_policy = SessionAuthenticationPolicy(callback=build_avatar)
    acl_policy = ACLAuthorizationPolicy()

    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings,
                          session_factory=session_factory,
                          authentication_policy=auth_policy,
                          authorization_policy=acl_policy,
                          root_factory=RootFactory
                          )
    config.add_static_view('static', 'crmbase:static', cache_max_age=3600)
    config.add_route('index', '/')

    # REST API
    ## using the four HTTP methods (POST, GET, PUT, DELETE),
    ## translating them in (add, get, update, delete)
    ## and the two following routes,
    ## we can get a very clean REST API
    config.add_route("users", "/users")
    config.add_route("user", "/users/{uid}")
    config.add_route("contacts", "/contacts")
    config.add_route("login", "/login")
    config.add_route("logout", "/logout")
    return config.make_wsgi_app()
