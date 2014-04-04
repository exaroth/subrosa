# -*- coding: utf-8 -*-
"""

    main.models.UsersModel
    ======================
    
    Implements model and methods related to user interaction

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.


"""

import os, sys
import datetime
from peewee import *

from main import db
from main.models.BaseModel import BaseModel
from main.helpers import handle_errors
from werkzeug.security import generate_password_hash, check_password_hash


class Users(BaseModel):

    """
    Models and methods related to user database interaction 
    """

    username = CharField( max_length = 40, unique = True, index = True )
    hash = CharField()
    real_name = CharField(max_length = 40, null = True )
    description = TextField(null = True)



    @staticmethod
    def check_any_exist():
        """ Check if any users exist """
        return Users.get_count() > 0

    @staticmethod
    def check_exists(username):

        """ Check if user with given username already exists """

        return Users.select()\
                .where(Users.username == username)\
                .exists()

    @staticmethod
    def get_user(id):
        """ Get user by id """
        return Users.get_single("id", id)

    @staticmethod
    def get_user_by_username(username):

        """ Get user by his username , returns 0 if not exists """

        return Users.get_single("username", username)


    @staticmethod
    @db.commit_on_success
    def create_user(username, password, description = None, real_name = None):

        """ Create new user """

        try:
            return Users.create(username = username,\
                                hash = generate_password_hash(password),\
                                description = description,\
                                real_name = real_name).get_id()

        except:
            handle_errors("Error creating user")
            raise

    def check_password(self, password):

        """ Compare password against the one in db """

        return check_password_hash(self.hash, password)

    def __repr__(self):
        return "<User: %s>" % self.username

    class Meta:
        order_by = ("username",)
