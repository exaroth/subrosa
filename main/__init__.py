from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.markdown import Markdown

app = Flask(__name__)
app.config.from_object("main.config")
db = SQLAlchemy(app)
Markdown(app,
	extensions = ["footnotes", "fenced_code", "codehilite" ])
from main import views, models


