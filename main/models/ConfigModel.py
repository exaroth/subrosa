

from peewee import *

from main import db
from main.models.BaseModel import BaseModel
from main.helpers import handle_errors


class ConfigModel(BaseModel):


    twitter     = TextField(null       = True, default = None)
    facebook    = TextField(null       = True, default = None)
    github      = TextField(null       = True, default = None)
    google_plus = TextField(null       = True, default = None)
    email       = TextField(null       = True, default = None)
    imgur_id    = TextField(null       = True, default = None)
    disqus      = TextField(null       = True, default = None)
    title       = TextField(null       = True, default = None)
    gallery     = BooleanField(default = False)
    projects    = BooleanField(default = False)
    show_info   = BooleanField(default = False)

    def save_settings(self, **kwargs):
        """
        Update settings given a dictionary of values
        """
        to_save = dict()
        for key, value in kwargs.items():
            if key in self._meta.get_field_names() and value is not None:
                to_save[key] = value
        try:
            print to_save
            for k, v in to_save.items():
                setattr(self, k, v)
            self.save()

        except Exception as e:
            handle_errors("Error updating configuration")
            raise
    
    @staticmethod
    def create_config(**kwargs):

        to_create = dict()

        for key, value in kwargs.items():
            if key in ConfigModel._meta.get_field_names() and value is not None:
                to_create[key] = value
        try:
            ConfigModel.create(**to_create)
            return 1
        except Exception as e:
            handle_errors("Error creating config file... Aborting")
            raise



