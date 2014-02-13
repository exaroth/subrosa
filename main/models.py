from main import app, db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from .helpers import slugify
from webhelpers.text import truncate
import os


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(120), unique = True)
    real_name = db.Column(db.String(120), nullable = True)
    hash = db.Column(db.String(120))


    def __init__(self, username, email, real_name, password):
        self.username = username
        self.email = email
        self.real_name = real_name
        self.hash = generate_password_hash(password)

    @property
    def get_articles(self):
        return self.articles.order_by("date_created").all()

    def check_password(self, password):
        return check_password_hash(self.hash, password)

    def __repr__(self):
        return "<User: {0}>".format(self.username)


class Articles(db.Model):

    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    slug = db.Column(db.String(120))
    draft = db.Column(db.Boolean, default = True)
    date_created = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    date_updated = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = db.relationship("User", backref = db.backref("articles", lazy = "dynamic"))

    def __init__(self, title, body, draft, author):
        self.title = title
        self.slug = slugify(title)
        self.draft = draft
        self.body = body
        self.author = author


    @staticmethod
    def get_article_by_author(name):
        return Articles.query.join(Users).\
                filter(Users.username == name).\
                order_by("date_created").all()

    def __repr__(self):
        return "<Article: {0}>".format(truncate(self.title))

class UserImages(db.Model):

    __tablename__ = "user_images"
    
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(120), unique = True)
    thumbnail = db.Column(db.String(120))
    showcase = db.Column(db.String(120))
    gallery = db.Column(db.Boolean, default = False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner = db.relationship("User", backref = db.backref("user_images", lazy = "dynamic"))

    def __init__(self, filename, thumbnail, showcase, gallery, owner):
        self.filename = filename
        self.thumbnail = thumbnail
        self.showcase = showcase
        self.gallery = gallery
        self.owner = owner

    def __repr__(self):
        return "<Image: {0}>".format(self.filename)

class ArticleTags(db.Model):

    __tablename__ = "article_tags"

    id = db.Column(db.Integer, primary_key = True)
    tag_name = db.Column(db.String(30), unique = True, nullable = False)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"))
    article = db.relationship("Articles", backref = db.backref("article_tags", lazy = "dynamic"))

    def __init__(self, tag_name, article):
        self.tag_name = tag_name
        self.article = article

    def __repr__(self):
        return "<Tag Name: {0}".format(self.tag_name)
