# -*- coding: utf-8 -*-
"""

    subrosa.subrosa_init
    ================

    Implements subrosa intiialization class


    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.

"""

from __future__ import absolute_import
from peewee import SqliteDatabase, PostgresqlDatabase, MySQLDatabase
from subrosa.filters import timesince
from subrosa.helpers import generate_csrf_token
from subrosa.markdown_ext import Markdown
from subrosa.helpers import logger
import logging
import os
import sys
from six.moves.urllib import parse


logging.basicConfig()


class Subrosa(object):

    """
    Initialization class for Subrosa
    Expects an instance of Flask application
    to be passed in constructor
    """

    OPTIONS = ("disqus", "facebook", "twitter", "github",
               "google_plus", "email", "gallery", "projects",
               "dynamic_site", "title", "articles_per_page",
               "images_per_page", "imgur_id", "thumbnail_size",
               "show_info", "twitter_username", "about")

    IMAGES = ('bg', 'logo', 'portrait')

    def __init__(self, app):

        self.app = app
        self.settings = dict()

        self.db_types = dict(
            sqlite=SqliteDatabase,
            postgres=PostgresqlDatabase,
            mysql=MySQLDatabase
        )
        # List of options that should be passed to views

        for option in self.OPTIONS:
            self.settings[option] = app.config.get(option.upper(), None)

        self._get_user_images()
        self._favicon_check()

        md = Markdown(app, extensions=["fenced_code",
                                       "codehilite",
                                       "headerid",
                                       "subrosa.md_extensions.extended_images"])

        app.jinja_env.globals['csrf_token'] = generate_csrf_token
        app.jinja_env.filters['timesince'] = timesince
        app.jinja_env.filters['markdown'] = md._build_filter(auto_escape=False)

    def _get_user_images(self):
        """ Check if user provided images exist in /uploads folder """
        for name in self.IMAGES:
            self.settings[name] = None
            for ext in self.app.config["ALLOWED_FILENAMES"]:
                filename = name + "." + ext
                path = os.path.join(self.app.config["UPLOAD_FOLDER"], filename)
                if os.path.exists(path):
                    self.settings[name] = filename

    def _select_db(self, db_type):

        db = self.db_types.get(db_type, None)
        if not db:
            raise OSError("==========Wrong database name selected===========")
        return db

    def _define_db_connection(self, db_type, db_name, **kwargs):

        try:
            db_conn = self._select_db(db_type)
            db = db_conn(db_name, **kwargs)
            return db
        except:
            raise

    def _favicon_check(self):
        """ Check for favicon """
        favicon_exists = os.path.exists(os.path.join(self.app.config["UPLOAD_FOLDER"],
                                                     "favicon.ico"))
        self.settings["favicon"] = True if favicon_exists else False

    def get_db(self, kwargs=dict()):

        """
        Return a new database connection object
        provided values defined in configuration file
        """
        # config for heroku
        if "DATABASE_URL" in os.environ:
            url = parse.urlparse(os.environ.get("DATABASE_URL"))
            DATABASE = {
                "database": url.path[1:],
                "user": url.username,
                "password": url.password,
                "host": url.hostname,
                "port": url.port
            }
            return PostgresqlDatabase(**DATABASE)
        dtype = self.app.config.get("DATABASE", None)
        dname = self.app.config.get("DATABASE_NAME", None)
        if self.app.config.get("TESTING", False):
            return self._define_db_connection("sqlite", ":memory:")
        if not dtype or not dname:
            raise ValueError("Database type and name must be defined")
        if dtype in ("postgres", "mysql"):
            username = self.app.config.get("DB_USERNAME")
            password = self.app.config.get("DB_PASSWORD", None)
            if not username:
                raise ValueError("%s requires username to connect" % dtype)
            kwargs.update(dict(
                user=username,
            ))
            if password:
                if dtype == "postgres":
                    kwargs.update(dict(
                        password=password
                    ))
                elif dtype == "mysql":
                    kwargs.update(dict(
                        passwd=password
                    ))
        try:
            return self._define_db_connection(dtype, dname, **kwargs)
        except Exception as e:
            logger.debug(e)

    def get_settings(self):
        return self.settings
