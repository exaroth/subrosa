

from peewee import *

from main.helpers import handle_errors
from main import db
from main.models.BaseModel import BaseModel


class ConfigModel(BaseModel):


    twitter        = TextField(null       = True, default = None)
    facebook       = TextField(null       = True, default = None)
    github         = TextField(null       = True, default = None)
    gplus          = TextField(null       = True, default = None)
    email          = TextField(null       = True, default = None)
    imgur          = TextField(null       = True, default = None)
    disqus         = TextField(null       = True, default = None)
    show_gallery   = BooleanField(default = False)
    show_projects  = BooleanField(default = False)
    show_user_info = BooleanField(default = False)

    def save_settings(self, **kwargs):
        
        to_save = dict()
        for key, value in kwargs:
            if key in self._meta.get_field_names():
                to_save[key] = value

        







