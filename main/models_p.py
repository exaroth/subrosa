from peewee import *

from main import app

from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from .helpers import handle_errors
from webhelpers.text import truncate



def select_db(db_type):


    db_types = dict(
        sqlite = SqliteDatabase,
        postrges = PostgresqlDatabase,
        mysql = MySQLDatabase
    )


    db = db_types.get(db_type, None)

    if not db:
        raise ValueError("Wrong database name selected")
    return db


def define_db_connection(db_type, db_name, **kwargs):
    try:
        db_conn = select_db(db_type)
        db = db_conn(db_name, kwargs)
        return db
    except:
        raise


# Put it into init

db = None
if app.config.get("DEBUG", False):
    db = define_db_connection("sqlite", ":memory:")
else:
    dtype = app.config.get("DB_NAME", None)
    dname = app.config.get("DATABASE_NAME", None)
    if not dtype or not dname:
        raise ValueError("Database type and name must be defined")
    try:
        # Get additional arguments
        db = define_db_connection(dtype, dname)
    except:
        raise


class BaseModel(Model):

    class Meta:
        database = db


class Users(BaseModel):

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
    def check_exists(username, email):

        """ Check if user with given username or email already exists """

        return Users.select()\
                .where((Users.username == username) | (Users.email == email))\
                .exists()

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
        ordering = ("username")


class Articles(BaseModel):

    title = TextField(unique = True)
    slug = TextField()






