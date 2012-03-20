# -*- coding: utf-8 -*-
# * File Name : auth.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 19-03-2012
# * Last Modified :
#
# * Project :
#
"""
    Form schema used for authentication
"""
import colander
import logging
from deform import widget

from crmbase.models import DBSESSION
from crmbase.models.model import User

log = logging.getLogger(__name__)
def auth(form, value):
    """
        Check the login/password content
    """
    log.debug(u" * Authenticating")
    db = DBSESSION()
    login = value.get('login')
    log.debug(u"   +  Login {0}".format(login))
    password = value.get('password')
    result = db.query(User).filter_by(login=login).first()
    log.debug(result)
    if not result or not result.authenticate(password):
        log.debug(u"    - Authentication Error")
        message = u"Erreur d'authentification"
        exc = colander.Invalid(form, message)
        exc['password'] = message
        raise exc

class FAuth(colander.MappingSchema):
    """
        Schema for authentication form
    """
    login = colander.SchemaNode(colander.String(),
                                    title="Identifiant")
    password = colander.SchemaNode(colander.String(),
                                       widget=widget.PasswordWidget(),
                                       title="Mot de passe")
    nextpage = colander.SchemaNode(colander.String(),
                                   widget=widget.HiddenWidget(),
                                   missing=u"")
authSchema = FAuth(validator=auth)
