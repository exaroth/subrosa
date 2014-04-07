

from peewee import *

from subrosa import db
from subrosa.models.BaseModel import BaseModel
from subrosa.helpers import handle_errors


class ConfigModel(BaseModel):

    
    """
    Class defining Subrosa configuration fields
    """


    twitter = TextField(null = True, default = "") # twitter address
    facebook = TextField(null = True, default = "") # facebook address
    github  = TextField(null = True, default = "") # github address
    google_plus = TextField(null = True, default = "") # g+ adress
    email = TextField(null = True, default = "") # email address
    imgur_id = TextField(null = True, default = "") # imgur user_id
    disqus = TextField(null = True, default = "") # disqus site_shortname
    title  = TextField(null = True, default = "") # site title
    twitter_username = TextField(null = True, default = "") 
    gallery = BooleanField(default = False) # show gallery
    projects = BooleanField(default = False) # show projects
    about = BooleanField(default = False) # show about page
    show_info = BooleanField(default = False) # show user info

    def save_settings(self, **kwargs):

        """
        Update settings given a dictionary of values
        """

        to_save = dict()
        for key, value in kwargs.items():
            if key in self._meta.get_field_names() and value is not None:
                to_save[key] = value
        try:
            for k, v in to_save.items():
                setattr(self, k, v)
            self.save()

        except Exception as e:
            handle_errors("Error updating configuration")
            raise
    
    @staticmethod
    def create_config(**kwargs):

        """ Create new config """

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



