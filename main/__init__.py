from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.markdown import Markdown
from flask.ext.cache import Cache
from werkzeug.contrib.cache import SimpleCache



app = Flask(__name__)
app.config.from_object("main.config")
db = SQLAlchemy(app)
cache = Cache(app)
c = SimpleCache()
Markdown(app,
	extensions = ["footnotes", "fenced_code", "codehilite" ])
from main import views, models

settings = dict()

settings["facebook"] = app.config.get("FACEBOOK", False)
settings["twitter"] = app.config.get("TWITTER", False)
settings["github"] = app.config.get("GITHUB", False)
settings["gallery"] = app.config.get("GALLERY", False)
settings["dynamic"] = app.config.get("DYNAMIC_SITE", False)
settings["title"] = app.config.get("SITE_TITLE", "Awesome site")
settings["articles_per_page"] = app.config.get("ARTICLES_PER_PAGE", 3)
