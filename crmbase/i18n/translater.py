# -*- coding: utf-8 -*-
# * File Name : translater.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 18-02-2012
# * Last Modified : lun. 19 mars 2012 15:50:30 CET
#
# * Project : crmbase
#
from pyramid.i18n import TranslationStringFactory
from pyramid.i18n import get_localizer

translater = TranslationStringFactory('crmbase')

def _(request, string, mapping=None):
    """
        returns the translated string regarding the current request's
        linguage
        Usage :
        _(request, "My test string")
    """
    ts = translater(string, mapping)
    localize = get_localizer(request)
    return localize.translate(ts)
