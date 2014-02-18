from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.markdown import Markdown
from flask.ext.cache import Cache

app = Flask(__name__)
app.config.from_object("main.config")
db = SQLAlchemy(app)
cache = Cache(app)
Markdown(app,
	extensions = ["footnotes", "fenced_code", "codehilite" ])
from main import views, models


