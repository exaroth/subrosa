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
from flask import Flask
from main.subrosa import Subrosa
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

app.config.update(
    BASE_PATH = BASE_PATH,
    ROOT_PATH = ROOT_PATH,
    UPLOAD_FOLDER = UPLOAD_FOLDER
)


cache = Cache(app)

subrosa = Subrosa(app)

settings = subrosa.get_settings()

db = subrosa.get_db()

from main import views
