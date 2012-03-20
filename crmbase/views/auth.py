# -*- coding: utf-8 -*-
# * File Name : auth.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : lun. 19 mars 2012 15:55:03 CET
#
# * Project :
#
"""
    Authentication related views
"""
import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from pyramid.httpexceptions import HTTPForbidden
from pyramid.security import authenticated_userid
from pyramid.security import forget
from pyramid.security import remember
from pyramid.security import NO_PERMISSION_REQUIRED

from deform import Form
from deform import Button
from deform import ValidationFailure

from crmbase.i18n import _
from crmbase.forms.auth import authSchema

log = logging.getLogger(__name__)

@view_config(context=HTTPForbidden, permission=NO_PERMISSION_REQUIRED)
def forbidden_view(request):
    """
        Custom forbidden view used to redirect anonymous users
        to the login form
    """
    log.debug("# Forbidden view")
    if authenticated_userid(request):
        log.debug(" + Authenticated but not allowed")
        return HTTPForbidden()
    log.debug(" + Not authenticated : try again")
    #redirecting to the login page with the current path as param
    loc = request.route_url('login', _query=(('nextpage', request.path),))
    return HTTPFound(location=loc)

@view_config(route_name='login', permission=NO_PERMISSION_REQUIRED,
                                                renderer='login.mako')
def login_view(request):
    """
        Login view
    """
    log.debug("# Login page")
    form = Form(authSchema,
                buttons=(Button(name="submit",
                                title="Valider",
                                type='submit'),))
    nextpage = request.params.get('nextpage') or request.route_url('index')
    app_struct = {'nextpage':nextpage}
    myform = form.render(app_struct)
    fail_message = None
    if 'submit' in request.params:
        log.debug(" + Validating authentication")
        controls = request.params.items()
        try:
            datas = form.validate(controls)
        except ValidationFailure, err:
            log.debug("Erreur d'authentification")
            myform = err.render()
            request.session.flash(_(request, u"Authentication error"), "error")
            return {'title':"Login page",
                    'form':myform,}
        log.debug("  + Validation ok, redirecting")
        log.debug("     -> {0}".format(nextpage))
        login = datas['login']
        # Storing the datas in the session
        remember(request, login)
        return HTTPFound(location=nextpage)
    return {
            'title':"Login page",
            'form':myform,
            'message':fail_message
            }

@view_config(route_name='logout', permission=NO_PERMISSION_REQUIRED)
def logout_view(request):
    """
        Logout view
    """
    headers = forget(request)
    loc = request.route_url('index')
    return HTTPFound(location=loc, headers=headers)
