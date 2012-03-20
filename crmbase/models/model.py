# -*- coding: utf-8 -*-
# * File Name : model.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : mer. 11 janv. 2012
# * Last Modified : lun. 19 mars 2012 15:18:19 CET
#
# * Project : crmbase
#
"""
    Models for our base crm
"""
from hashlib import sha224
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import func

from sqlalchemy.orm import relationship

from crmbase.models import DBBASE

CONTACTEMAILS = Table('contactemaillink', DBBASE.metadata,
                        Column('contact_id', Integer,
                                ForeignKey('contact.id')),
                        Column('contact_email_id', Integer,
                                ForeignKey('contact_email.id'))
                            )
CONTACTADDRESSES = Table("contactaddresslink", DBBASE.metadata,
                        Column('contact_id', Integer,
                                ForeignKey('contact.id')),
                        Column('contact_address_id', Integer,
                                ForeignKey('contact_address.id'))
                        )

def crypt(data):
    """
        Password encryption
    """
    if data:
        return sha224(data).hexdigest()
    else:
        return False

class TimeStamped(object):
    """
        Class with a timestamp attribute
        used to add a created_by attribute
    """
    created_at = Column(DateTime, default=func.now())

class User(TimeStamped, DBBASE):
    """
        User account
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    login = Column(String(255), unique=True)
    password = Column(String(255))

    contact = relationship("Person", uselist=False, backref="account")

    def __init__(self, login, password):
        self.login = login
        self.password = crypt(password)

    def authenticate(self, password):
        """
            Return True if the passwords match
        """
        return self.password == crypt(password)

class Contact(TimeStamped, DBBASE):
    """
        Contact object
    """
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True)

    # configure a field which will be used to manage polymorphism
    discriminator = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}

    emails = relationship("Email",
                            secondary=CONTACTEMAILS,
                            backref='contacts')

    addresses = relationship("Address",
                            secondary=CONTACTADDRESSES,
                            backref='contacts')

class Person(Contact):
    """
        contact as a person
    """
    __tablename__ = "person"
    __mapper_args__ = {'polymorphic_identity': 'person'}
    id = Column(Integer, ForeignKey('contact.id'), primary_key=True)
    firstname = Column(String(255))
    lastname = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, lastname, firstname=None, email=None):
        self.lastname = lastname
        if firstname:
            self.firstname = firstname
        if email:
            self.emails.append(Email(email))

    def add_account(self, login, password):
        # TODO:Check for unicity
        self.account = User(login, password)

class Company(Contact):
    """
        contact as a company
    """
    __tablename__ = "company"
    __mapper_args__ = {'polymorphic_identity': 'company'}
    id = Column(Integer, ForeignKey('contact.id'), primary_key=True)
    name = Column(String(255), nullable=False)
    sigle = Column(String(255))

class Email(DBBASE):
    """
        Email address object
    """
    __tablename__ = 'contact_email'
    id = Column(Integer, primary_key=True)
    address = Column(String(255), nullable=False, unique=True)
    comment = Column(String(255))

    def __init__(self, address, comment=None):
        self.address = address
        if comment:
            self.comment = comment

class Address(DBBASE):
    """
        Postal adress of a contact
    """
    __tablename__ = 'contact_address'
    id = Column(Integer, primary_key=True)
    field1 = Column(String(255))
    field2 = Column(String(255))
    postcode = Column(String(32))
    city = Column(String(32))
    country = Column(String(32))
    comment = Column(String(255))

    def __init__(self, field1, field2=None, postcode=None, city=None,
                                        country=None, comment=None):
        self.field1 = field1
        if field2:
            self.field2 = field2
        if postcode:
            self.postcode = postcode
        if city:
            self.city = city
        if country:
            self.country = country
        if comment:
            self.comment = comment

