# -*- coding: utf-8 -*-
# * File Name : views.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : mer. 11 janv. 2012
# * Last Modified : lun. 19 mars 2012 14:26:48 CET
#
# * Project : crmbase
#

from pyramid.view import view_config
from pyramid.url import route_url, route_path
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from crmbase.models import DBSESSION
from crmbase.models.model import User
from crmbase.i18n import _
# DBSESSION is used to access database:
#ex :
#    session = DBSESSION()
#    users = session.query(User).all()

@view_config(name='navigation', renderer='menu.mako')
def menu(request):
    """
        returns the main menu
    """
    #TODO : view/edit permission ...
    menu = (dict(label='Users',
                 url=route_path('users', request),
                 title="User management",
                 icon=""),
            dict(label='Contacts',
                 url=route_path('contacts', request),
                 title="Contact and relationships",
                 icon=""),
                 )
    return dict(menu=menu)

@view_config(route_name='index', renderer='index.mako')
def default_index(request):
    """
        Return only a title for the page
    """
    return dict(title="Default page for pyramid projects from Majerti")

@view_config(route_name='users', renderer='userlist.mako', request_method='GET')
def users(request):
    """
        Returns the list of all users
    """
    session = DBSESSION()
    users = session.query(User).all()
    return dict(title='UserList', users=users)

@view_config(route_name='user', renderer='user.mako', request_method='GET')
def user(request):
    """
        Return a user object
    """
    session = DBSESSION()
    user = session.query(User).filter_by(id=user_id).first()
    return dict(title='User', user='user')
