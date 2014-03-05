from flask import Flask
from main.subrosa import Subrosa
from flask.ext.cache import Cache
import os, sys
import logging
from jinja2htmlcompress import HTMLCompress


__version__ = "0.0.2.dev"

logger = logging.getLogger(__name__)


app = Flask(__name__)

# config init
app.config.from_object("main.default_config")
app.config.from_pyfile("../subrosa.conf")
if os.environ.get("SUBROSA_CONFIG"):
    app.config.from_envvar("SUBROSA_CONFIG", silent = False)

cache = Cache(app)


subrosa = Subrosa(app)

settings = subrosa.get_settings()

db = subrosa.get_db()

from main import views

