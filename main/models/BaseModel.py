# -*- coding: utf-8 -*-
"""

    main.models.BaseModel
    ============
    
    Base Database model used as a superclass 
    by other models

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.


"""
import os, sys


from peewee import *
from main import db

class BaseModel(Model):

    class Meta:
        database = db

