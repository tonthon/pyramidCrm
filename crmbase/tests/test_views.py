# -*- coding: utf-8 -*-
# * File Name : test_views.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 13-03-2012
# * Last Modified :
#
# * Project :
#
from crmbase.models.model import Person
from .base import BaseViewTest


class TestViews(BaseViewTest):
    """
        Test views
    """
    def add_dummy_user(self):
        user = Person('Dupont', firstname='admin')
        user.add_account("admin", 'password')
        self.session.add(user)
        self.session.flush()

    def test_login(self):
        self.add_dummy_user()
        from crmbase.views.auth import login_view
        self.config.add_route('index', '/')
        request = self.get_csrf_request(
                        dict(submit=True,
                              login='admin',
                              password='password',
                              ))
        response = login_view(request)
        assert response.status_int == 302

    def test_wrong_login(self):
        self.add_dummy_user()
        from crmbase.views.auth import login_view
        self.config.add_route('index', '/')
        request = self.get_csrf_request(
                        dict(submit=True,
                              login='wronglogin',
                              password='password',
                              ))
        response = login_view(request)
        assert request.session.pop_flash('error')

    def test_wrong_password(self):
        self.add_dummy_user()
        from crmbase.views.auth import login_view
        self.config.add_route('index', '/')
        request = self.get_csrf_request(
                        dict(submit=True,
                              login='admin',
                              password='wrongpassword',
                              ))
        response = login_view(request)
        assert request.session.pop_flash('error')

    def test_redirect(self):
        self.add_dummy_user()
        from crmbase.views.auth import login_view
        self.config.add_route('index', '/')
        request = self.get_csrf_request(
                        dict(submit=True,
                              login='admin',
                              password='password',
                              nextpage='/dummy'
                              ))
        response = login_view(request)
        assert response.status_int == 302
        assert '/dummy' in dict(response.headerlist).values()
