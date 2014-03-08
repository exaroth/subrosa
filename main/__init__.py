# -*- coding: utf-8 -*-
"""

        Subrosa - and elegant blogging platform
        written in Python and Flask microframework

        https://github.com/mitsuhiko/flask

        :copyright: (c) 2014 by Konrad Wasowicz
        :license: MIT, see LICENSE for details.

"""

__version__ = "0.2.dev"


import os, sys
import logging
from flask import Flask, request
from main.subrosa import Subrosa
from .helpers import add_thumbnail_affix
from flask.ext.cache import Cache


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.abspath(os.path.join(BASE_PATH , ".."))
UPLOAD_FOLDER = os.path.dirname(os.path.join(ROOT_PATH, "uploads/")) + "/"

logger = logging.getLogger(__name__)


app = Flask(__name__)

# config init
app.config.from_object("main.default_config")
app.config.from_pyfile("../subrosa.conf")
if os.environ.get("SUBROSA_CONFIG"):
    app.config.from_envvar("SUBROSA_CONFIG", silent = False)

if os.environ.get("CI"):
    app.config.update(dict(
    DATABASE = "sqlite",
    DATABASE_NAME = "test.db"
    ))

app.config.update(
    BASE_PATH = BASE_PATH,
    ROOT_PATH = ROOT_PATH,
    UPLOAD_FOLDER = UPLOAD_FOLDER
)


cache = Cache(app)

subrosa = Subrosa(app)

settings = subrosa.get_settings()

db = subrosa.get_db()

@app.context_processor
def utility_processor():
    return dict(settings = settings,\
                current_path = request.url_root + request.path[1:],\
                add_thumbnail_affix = add_thumbnail_affix)

from main.create_views import CreateArticleView, CreateProjectView
from main.edit_views import UpdateArticleView, UpdateProjectView

app.add_url_rule("/create-article/", view_func = CreateArticleView.as_view("create_article"))
app.add_url_rule("/create-project/", view_func = CreateProjectView.as_view("create_project"))
app.add_url_rule("/edit-article/<int:id>", view_func = UpdateArticleView.as_view("edit_article"))
app.add_url_rule("/edit-project/<int:id>", view_func = UpdateProjectView.as_view("edit_project"))


from main import views, misc
