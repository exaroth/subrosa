# -*- coding: utf-8 -*-
"""

    main.subrosa
    ============

    Implements subrosa intiialization class


    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.

"""
import pathlib
from filters import parse_img_tags, timesince
from helpers import generate_csrf_token
from peewee import SqliteDatabase, PostgresqlDatabase, MySQLDatabase
from main.markdown_ext import Markdown
from jinja2htmlcompress import HTMLCompress
import logging
import os, sys

logger = logging.getLogger("subrosa")


class Subrosa(object):

    """
    Initialization class for Subrosa
    """

    OPTIONS = ("disqus", "facebook", "twitter", "github", "google_plus", "email", "gallery", "dynamic_site", "title",\
                       "articles_per_page", "images_per_page", "imgur_id", "thumbnail_size")

    IMAGES = ('bg', 'bg_small', 'logo', 'portrait')

    def __init__(self, app, compress_html = False):

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

        self._get_user_images()
        self._favicon_check()

        md = Markdown(app,
                 extensions = [ "fenced_code",\
                               "codehilite",\
                               "headerid",\
                               "main.extended_images" ])

        if compress_html:
            app.jinja_env.add_extension(HTMLCompress)

        app.jinja_env.globals['csrf_token'] = generate_csrf_token
        app.jinja_env.filters['parse_img_tags'] = parse_img_tags
        app.jinja_env.filters['timesince'] = timesince
        app.jinja_env.filters['markdown'] = md._build_filter(auto_escape = False)


    def _get_user_images(self):
        for name in self.IMAGES:
            self.settings[name] = None
            for ext in self.app.config["ALLOWED_FILENAMES"]:
                filename = name + "." + ext
                path = os.path.join(self.app.config["UPLOAD_FOLDER"], filename )
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
        favicon = pathlib.Path(os.path.join(self.app.config["UPLOAD_FOLDER"], "favicon.ico"))
        self.settings["favicon"] = True if favicon.exists() else False


    def get_db(self, **kwargs):

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
            return  self._define_db_connection(dtype, dname, **kwargs)
        except:
            raise

    def get_settings(self):
        return self.settings
