# -*- coding: utf-8 -*-
# * File Name : __init__.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 18-02-2012
# * Last Modified : mar. 13 mars 2012 11:42:25 CET
#
# * Project : {{project}}
#

from sqlalchemy.ext import declarative
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from zope.sqlalchemy import ZopeTransactionExtension

DBBASE = declarative.declarative_base()
DBSESSION = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

def record_to_appstruct(self):
    """
        Transform a SQLAlchemy object into a deform compatible dict
        usefull to autofill an editform directly from db recovered datas
    """
    return dict([(k, self.__dict__[k])
                for k in sorted(self.__dict__) if '_sa_' != k[:4]])
DBBASE.appstruct = record_to_appstruct

def initialize_sql(engine, create=False):
    """
        Initialize the database engine
    """
    DBSESSION.configure(bind=engine)
    DBBASE.metadata.bind = engine
    DBBASE.metadata.create_all(engine)
