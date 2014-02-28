import os, sys


sys.path.append("..")

from peewee import *

from main import db




class BaseModel(Model):

    class Meta:
        database = db

