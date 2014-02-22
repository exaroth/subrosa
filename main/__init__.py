from flask import Flask
from flask.ext.markdown import Markdown
from flask.ext.cache import Cache
from peewee import SqliteDatabase, PostgresqlDatabase, MySQLDatabase



app = Flask(__name__)
app.config.from_object("main.config")
cache = Cache(app)
Markdown(app,
         extensions = ["footnotes", "fenced_code", "codehilite" ])

settings = dict()

settings["facebook"] = app.config.get("FACEBOOK", False)
settings["twitter"] = app.config.get("TWITTER", False)
settings["github"] = app.config.get("GITHUB", False)
settings["gallery"] = app.config.get("GALLERY", False)
settings["dynamic"] = app.config.get("DYNAMIC_SITE", False)
settings["title"] = app.config.get("SITE_TITLE", "Awesome site")
settings["articles_per_page"] = app.config.get("ARTICLES_PER_PAGE", 3)


def select_db(db_type):


    db_types = dict(
        sqlite = SqliteDatabase,
        postrges = PostgresqlDatabase,
        mysql = MySQLDatabase
    ) 

    db = db_types.get(db_type, None)

    if not db:
        raise ValueError("Wrong database name selected")
    return db


def define_db_connection(db_type, db_name, **kwargs):
    try:
        db_conn = select_db(db_type)
        db = db_conn(db_name, kwargs)
        return db
    except:
        raise


db = None
if app.config.get("TESTING", False):
    db = define_db_connection("sqlite", ":memory:")
else:
    dtype = app.config.get("DATABASE", None)
    dname = app.config.get("DATABASE_NAME", None)
    if not dtype or not dname:
        raise ValueError("Database type and name must be defined")
    try:
        # Get additional arguments
        db = define_db_connection(dtype, dname)
    except:
        raise

from main import views, models
