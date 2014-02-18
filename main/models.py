# -*- coding: utf-8 -*-

"""
    Database models file for Subrosa

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: BSD, see LICENSE for more details

"""



from main import app, db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from .helpers import slugify, handle_errors
from webhelpers.text import truncate
import os
from sqlalchemy.sql import exists


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

    @staticmethod
    def add_user(username, email, password, real_name):
        new_user = User(username = username,\
                        password = password,\
                        email = email, \
                        real_name = real_name)

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            handle_errors("Error creating user")
            raise

    @staticmethod
    def get_user_by_username(username):
        try:
            return User.query.filter_by(username = username).first()
        except Exception as e:
            handle_errors(e)

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
    def paginate_articles(page, pages_per_page):
        try:
            return Articles.query.\
                    order_by(Articles.date_created.desc()).\
                    paginate(page, pages_per_page)
        except:
            handle_errors()

    @staticmethod
    def get_user_articles(user):
        try:
            return Articles.query.\
                    filter_by(author = user).\
                    order_by(Articles.date_created.desc()).\
                    all()
        except Exception as e:
            handle_errors()

    @staticmethod
    def check_exists(title):
        try:
            return db.session.query(exists().where(Articles.title == title)).scalar()
        except:
            db.session.rollback()
            handle_errors()



    @staticmethod
    def create_article(title, body, author, draft):
        new_article = Articles(title = title,\
                               body = body,\
                               author = author,\
                               draft = draft)

        try:
            db.session.add(new_article)
            db.session.commit()
        except Exception as e:
            db.sessin.rollback()
            handle_errors("Error creating article")

    @staticmethod
    def update_article(article, title, body):
        article.title = title
        article.body = body
        article.date_updated = datetime.datetime.utcnow()
        try:
            db.session.add(article)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            handle_errors("Error updating article")

    @staticmethod
    def publish_article(article):
        try:
            article.draft = False
            db.session.add(article)
            db.session.commit()

        except:
            db.session.rollback()
            handle_errors()


    @staticmethod
    def delete_article(article):
        try:
            db.session.delete(article)
            db.session.commit()
        except:
            db.session.rollback()
            handle_errors()

    def __repr__(self):
        return "<Article: {0}>".format(truncate(self.title))

class UserImages(db.Model):

    __tablename__ = "user_images"
    
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(120), unique = True)
    showcase = db.Column(db.String(120))
    description = db.Column(db.String(120), nullable = True)
    is_vertical = db.Column(db.SmallInteger)
    gallery = db.Column(db.Boolean, default = False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner = db.relationship("User", backref = db.backref("user_images", lazy = "dynamic"))

    def __init__(self, filename, showcase, description, is_vertical, gallery, owner):
        self.filename = filename
        self.description = description
        self.is_vertical = is_vertical
        self.showcase = showcase
        self.gallery = gallery
        self.owner = owner

    @staticmethod
    def add_image(filename, showcase, description, is_vertical, gallery, owner):
        try:
            user_image = UserImages(filename = filename,\
                                    showcase = showcase,\
                                    description = description,\
                                    is_vertical = is_vertical,\
                                    gallery = gallery,\
                                    owner = owner)
            db.session.add(user_image)
            db.session.commit()
        except:
            db.session.rollback()
            handle_errors("Error creating image")
            raise
    @staticmethod
    def delete_image(image):
        try:
            db.session.delete(image)
            db.session.commit()
        except:
            db.session.rollback()
            handle_errors("Error deleting image")
            raise

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
