# -*- coding: utf-8 -*-
"""

        Subrosa - and elegant blogging platform
        written in Python and Flask microframework

        https://github.com/mitsuhiko/flask

        :copyright: (c) 2014 by Konrad Wasowicz
        :license: MIT, see LICENSE for details.

"""

from __future__ import absolute_import


__version__ = "0.1.dev"
__author__ = "Konrad Wasowicz"


import os
import sys
import logging
from flask import Flask, request
from subrosa.subrosa_init import Subrosa
from subrosa.helpers import add_thumbnail_affix
from flask.ext.cache import Cache


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.abspath(os.path.join(BASE_PATH, ".."))
UPLOAD_FOLDER = os.path.dirname(os.path.join(ROOT_PATH, "uploads/")) + "/"

logger = logging.getLogger(__name__)


app = Flask(__name__)

# config init
app.config.from_object("subrosa.default_config")
app.config.from_pyfile("../subrosa.conf")
if os.environ.get("SUBROSA_CONFIG"):
    # Get development config stored in ~/.configs/subrosa.py
    app.config.from_envvar("SUBROSA_CONFIG", silent=False)

if os.environ.get("CI"):
    # Configuration for travis
    app.config.update(dict(
        DATABASE="sqlite",
        DATABASE_NAME="test.db",
        TESTING=True
    ))

app.config.update(
    BASE_PATH=BASE_PATH,
    ROOT_PATH=ROOT_PATH,
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    STATIC_ROOT=app.config["DEBUG"] and "src/" or "build/"
)


cache = Cache(app)

s = Subrosa(app)

settings = s.get_settings()

db = s.get_db()

from subrosa.models.ConfigModel import ConfigModel


def get_config():

    """
    This function provides configuration
    dictionary to views. If config exists
    in cache returns it otherwise preforms
    query to db and sets the cache. If cache
    doesn't exist creates new config object.
    """

    c = cache.get("configuration")
    if not c:
        try:
            config = ConfigModel.select().get()
            cache.set("configuration", config)
            return config
        except:
            logger.info("No configuration table found in db, creating new one")
            try:
                ConfigModel.create_config(**settings)
                config = ConfigModel.select().get()
                cache.set("configuration", config)
                return config
            except Exception as exc:
                raise Exception("Error when creating config file...
                                aborting\n Error: {0}".format(exc))
    return c


@app.context_processor
def utility_processor():
    """
    Appends additional data to default context
    settings - basic Subrosa config fields
    current_path - full url to current view
    add_thumbnail_affix (fn) - function used
    for adding affix for imgur thumbnails
    """
    return dict(settings=get_config(),
                current_path=request.url_root + request.path[1:],
                add_thumbnail_affix=add_thumbnail_affix)

from subrosa.views.create_views import CreateArticleView, CreateProjectView
from subrosa.views.edit_views import UpdateArticleView, UpdateProjectView

app.add_url_rule("/create-article/", view_func=CreateArticleView.as_view("create_article"))
app.add_url_rule("/create-project/", view_func=CreateProjectView.as_view("create_project"))
app.add_url_rule("/edit-article/<int:id>", view_func=UpdateArticleView.as_view("edit_article"))
app.add_url_rule("/edit-project/<int:id>", view_func=UpdateProjectView.as_view("edit_project"))

from subrosa.views import main_views
from subrosa import misc
