from flask import Flask
from main.markdown_ext import Markdown
from flask.ext.cache import Cache
from peewee import SqliteDatabase, PostgresqlDatabase, MySQLDatabase
import pathlib
import os, sys
import logging
from jinja2htmlcompress import HTMLCompress
from filters import parse_img_tags, timesince
from helpers import generate_csrf_token


__version__ = "0.0.2.dev"

logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config.from_object("main.default_config")
app.config.from_pyfile("../subrosa.cfg")
if os.environ.get("SUBROSA_CONFIG"):
    app.config.from_envvar("SUBROSA_CONFIG", silent = False)

cache = Cache(app)
md = Markdown(app,
         extensions = [ "fenced_code", "codehilite", "headerid", "main.extended_images" ],\
         )




class Subrosa(object):

    """
    Initialization class for Subrosa 
    """

    OPTIONS = ("disqus", "facebook", "twitter", "github", "gallery", "dynamic_site", "title",\
                       "articles_per_page", "images_per_page", "imgur_id", "thumbnail_size")

    IMAGES = ('bg', 'bg_small', 'logo', 'portrait')

    def __init__(self, app, compress_html = False):

        self.settings = dict()

        self.db_types = dict(
            sqlite = SqliteDatabase,
            postrges = PostgresqlDatabase,
            mysql = MySQLDatabase
        ) 
        # List of options that should be passed to views

        for option in self.OPTIONS:
            self.settings[option] = app.config.get(option.upper(), None)

        self._get_user_images()
        self._favicon_check()

        if compress_html:
            app.jinja_env.add_extension(HTMLCompress)

        app.jinja_env.globals['csrf_token'] = generate_csrf_token  
        app.jinja_env.filters['parse_img_tags'] = parse_img_tags
        app.jinja_env.filters['timesince'] = timesince
        app.jinja_env.filters['markdown'] = md._build_filter(auto_escape = True)


    def _get_user_images(self):
        for name in self.IMAGES:
            self.settings[name] = None
            for ext in app.config["ALLOWED_FILENAMES"]:
                filename = name + "." + ext
                path = os.path.join(app.config["UPLOAD_FOLDER"], filename )
                if self._user_img_exists(path):
                    self.settings[name] = filename

    def _user_img_exists(self, file):
        p = pathlib.Path(file)
        if p.exists():
            return True
        return False

    def _select_db(self, db_type):
        db = self.db_types.get(db_type, None)

        if not db:
            raise ValueError("Wrong database name selected")
        return db

    def _define_db_connection(self, db_type, db_name, **kwargs):

        try:
            db_conn = self._select_db(db_type)
            db = db_conn(db_name, **kwargs)
            return db
        except:
            raise

    def _favicon_check(self):
        favicon = pathlib.Path(os.path.join(app.config["UPLOAD_FOLDER"], "favicon.ico"))
        self.settings["favicon"] = True if favicon.exists() else False


    def get_db(self, **kwargs):

        if app.config.get("TESTING", False):
            db = self._define_db_connection("sqlite", ":memory:")
        else:
            dtype = app.config.get("DATABASE", None)
            dname = app.config.get("DATABASE_NAME", None)
            if not dtype or not dname:
                raise ValueError("Database type and name must be defined")
            if dtype in ("postgres", "mysql"):
                username = app.config.get("DB_USERNAME")
                password = app.config.get("DB_PASSWORD", None)
                if not username:
                    raise ValueError("%s requires username to connect" % dtype)
                kwargs["user"] = username
                kwargs["password"] = password
            try:
                return  self._define_db_connection(dtype, dname, **kwargs)
            except:
                raise
    
    def get_settings(self):
        return self.settings



subrosa = Subrosa(app)

settings = subrosa.get_settings()

db = subrosa.get_db()

from main import views

