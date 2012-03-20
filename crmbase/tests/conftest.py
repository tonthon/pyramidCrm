# -*- coding: utf-8 -*-
# * File Name : conftest.py
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


def pytest_sessionstart():
    """
        Py.test setup
    """
    from py.test import config

    # Only run database setup on master (in case of xdist/multiproc mode)
    if not hasattr(config, 'slaveinput'):
        from crmbase.models import initialize_sql
        from crmbase.models.model import *
        from pyramid.config import Configurator
        from paste.deploy.loadwsgi import appconfig
        from sqlalchemy import engine_from_config
        import os

        root_path = os.path.dirname(__file__)
        settings = appconfig('config:' + os.path.join(root_path, "../../",
                                                                'test.ini'),
                                                        "crmbase")
        engine = engine_from_config(settings, prefix='sqlalchemy.')

        print 'Creating the tables on the test database %s' % engine

        config = Configurator(settings=settings)
        initialize_sql(engine, create=True)
