import os, sys

sys.path.append("..")

from peewee import *
from BaseModel import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from main.helpers import handle_errors
import datetime
from main import db


class Users(BaseModel):

    """
    Models and methods related to user database interaction 
    """

    username = CharField( max_length = 40, unique = True, index = True )
    email = CharField(max_length = 40, unique = True )
    hash = CharField()
    real_name = CharField(max_length = 40, null = True )


    @staticmethod
    @db.commit_on_success
    def create_user(username, email, password, real_name = None):

        """ Create new user """

        try:
            return Users.create(username = username, email = email, hash = generate_password_hash(password), real_name = real_name).get_id()

        except:
            handle_errors("Error creating user")
            raise

    @staticmethod
    def check_any_exist():
        return len(list(Users.select())) > 0

    @staticmethod
    def check_exists(username, email):

        """ Check if user with given username or email already exists """

        return Users.select()\
                .where((Users.username == username) | (Users.email == email))\
                .exists()

    @staticmethod
    def get_user(id):
        try:
            return Users.select().where(Users.id == id).get()
        except:
            return 0

    @staticmethod
    def get_user_by_username(username):

        """ Get user by his username , returns 0 if not exists """

        try:
            return Users.select().where(Users.username == username).get()
        except:
            return 0

    def check_password(self, password):

        """ Compare password against the one in db """

        return check_password_hash(self.hash, password)

    def __repr__(self):
        return "<User: %s>" % self.username

    class Meta:
        order_by = ("username",)
