# -*- coding: utf-8 -*-
"""

    subrosa.models.BaseModel
    ============

    Base Database model used as a superclass
    by other models

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.


"""

from peewee import *
from subrosa import db


class BaseModel(Model):

    @classmethod
    def get_single(cls, column, identifier):
        """ Get item by an identifier or return 0"""
        try:
            return cls.select().where(getattr(cls, column) == identifier).get()
        except:
            return 0

    @classmethod
    def get_count(cls):
        try:
            return cls.select().count()
        except:
            raise

    class Meta:
        database = db
