# -*- coding: utf-8 -*-
# * File Name : test_models.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 12-03-2012
# * Last Modified :
#
# * Project :
#
from .base import BaseTestCase

class TestContact(BaseTestCase):
    def test_email(self):
        from crmbase.models.model import Person, Email
        a = Person(lastname="Dupont", firstname="Jean", email='jean@dupont.fr')
        self.assertEqual(a.emails[0].address, "jean@dupont.fr")

    def test_address(self):
        from crmbase.models.model import Person, Address
        a = Person(lastname="Dupont", firstname="Jean", email='jean@dupont.fr')
        address = Address("1 cours de la liberté", postcode="69003",
                                                   city="Lyon",
                                                   comment='Home')
        a.addresses.append(address)
        self.assertEqual(a.addresses[0].comment, 'Home')
        self.assertEqual(a.addresses[0].postcode, '69003')

    def test_account(self):
        from crmbase.models.model import Person
        a = Person(lastname="Dupont", firstname="Jean", email='jean@dupont.fr')
        a.add_account('admin', "password")
        a.account.authenticate("password")

    def test_timestamp(self):
        from crmbase.models.model import Person
        import datetime
        now = datetime.datetime.utcnow()
        a = Person(lastname="Dupont", firstname="Jean", email='jean@dupont.fr')
        self.session.add(a)
        self.trans.commit()
        saved = self.session.query(Person).filter_by(lastname="Dupont").first()
        elapsed = now - saved.created_at
        one = datetime.timedelta(seconds=3)
        self.assertTrue(elapsed<one)

class TestUser(BaseTestCase):
    def test_auth(self):
        from crmbase.models.model import User
        a = User("jean.dupont", "password")
        self.assertTrue(a.authenticate("password"))
        self.assertFalse(a.authenticate("wrongpass"))
        self.assertFalse(a.authenticate(None))
