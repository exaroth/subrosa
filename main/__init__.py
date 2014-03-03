from flask import Flask
from flask.ext.markdown import Markdown
from flask.ext.cache import Cache
from peewee import SqliteDatabase, PostgresqlDatabase, MySQLDatabase
import pathlib
import os, sys
import logging
from jinja2htmlcompress import HTMLCompress


__version__ = "0.0.2.dev"

logger = logging.getLogger(__name__)



app = Flask(__name__)
app.config.from_object("main.default_config")
app.config.from_pyfile("../subrosa.cfg")

cache = Cache(app)
Markdown(app,
         extensions = [ "fenced_code", "codehilite", "main.extended_images" ],\
         )

# app.jinja_env.add_extension(HTMLCompress)



class Subrosa(object):

    """
    Initialization class for Subrosa 
    """

    OPTIONS = ("disqus", "facebook", "twitter", "github", "gallery", "dynamic_site", "title",\
                       "articles_per_page", "images_per_page", "imgur_id", "thumbnail_size")

    IMAGES = ('bg', 'bg_small', 'logo', 'portrait')

    def __init__(self, app = None):

        self.app = app
        self.settings = dict()

        self.db_types = dict(
            sqlite = SqliteDatabase,
            postrges = PostgresqlDatabase,
            mysql = MySQLDatabase
        ) 
        # List of options that should be passed to views

        for option in self.OPTIONS:
            self.settings[option] = app.config.get(option.upper(), None)

        self.get_user_images()



    def get_user_images(self):
        for name in self.IMAGES:
            self.settings[name] = None
            for ext in self.app.config["ALLOWED_FILENAMES"]:
                filename = name + "." + ext
                path = os.path.join(app.config["UPLOAD_FOLDER"], filename )
                if self.user_img_exists(path):
                    self.settings[name] = filename

    def user_img_exists(self, file):
        p = pathlib.Path(file)
        if p.exists():
            return True
        return False

    def select_db(self, db_type):
        db = self.db_types.get(db_type, None)

        if not db:
            raise ValueError("Wrong database name selected")
        return db

    def define_db_connection(self, db_type, db_name, **kwargs):
        try:
            db_conn = self.select_db(db_type)
            db = db_conn(db_name, **kwargs)
            return db
        except:
            raise

    def get_db(self, **kwargs):

        if self.app.config.get("TESTING", False):
            db = define_db_connection("sqlite", ":memory:")
        else:
            dtype = self.app.config.get("DATABASE", None)
            dname = self.app.config.get("DATABASE_NAME", None)
            if not dtype or not dname:
                raise ValueError("Database type and name must be defined")
            if dtype in ("postgres", "mysql"):
                username = self.app.config.get("DB_USERNAME")
                password = self.app.config.get("DB_PASSWORD", None)
                if not username:
                    raise ValueError("%s requires username to connect" % dtype)
                kwargs["user"] = username
                kwargs["password"] = password
            try:
                return  self.define_db_connection(dtype, dname, **kwargs)
            except:
                raise
    
    def get_settings(self):
        return self.settings



subrosa = Subrosa(app)

settings = subrosa.get_settings()

db = subrosa.get_db()

from main import views, models
from filters import parse_img_tags, timesince
from helpers import generate_csrf_token

app.jinja_env.globals['csrf_token'] = generate_csrf_token  
app.jinja_env.filters['parse_img_tags'] = parse_img_tags
app.jinja_env.filters['timesince'] = timesince
