# -*- coding: utf-8 -*-
"""

    main.models.ArticlesModel
    ============
    
    Implements model and methods related to subrosa articles

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.


"""

from __future__ import absolute_import

import os, sys
from peewee import *
import datetime

from main import db
from main.helpers import handle_errors, slugify
from main.models.BaseModel import BaseModel
from main.models.UsersModel import Users




class Articles(BaseModel):

    """
    Models and methods related to articles
    """

    title = CharField(unique = True)
    slug = CharField(unique = True)
    draft = BooleanField(default = True)
    date_created = DateTimeField(default = datetime.datetime.utcnow())
    date_updated = DateTimeField(default = datetime.datetime.utcnow())
    body = TextField()
    author = ForeignKeyField(Users, related_name = "articles")

    @staticmethod
    def get_article(id):
        try:
            return Articles.select().where(Articles.id == id).get()
        except:
            return 0

    @staticmethod
    def get_count(drafts = False):
        """ Return number of articles """
        q = Articles.select()
        if drafts:
            return q.count()
        return q.where(Articles.draft == False).count()
    
    @staticmethod
    def get_index_articles(page, per_page):
        """ Returns paginated articles for the index page"""

        try:
            return Articles\
                    .select()\
                    .where(Articles.draft == False)\
                    .paginate(page, per_page)
        except:
            handle_errors("Error getting articles")

    @staticmethod
    def get_user_articles(username):

        """ Get all articles belonging to user """

        try:
            return Articles.select()\
                    .join(Users)\
                    .where(Users.username == username)

        except:
            handle_errors("Error getting articles")

    @staticmethod
    def check_exists(title, id = False):

        """
        Check if article exists, if id is given checks if title 
        of article has different id (for updating articles)
        """

        try:
           q =  Articles.select().where((Articles.title == title))
           if not id:
               return q.get()
           return q.where(Articles.id != id).get()
        except:
            return False

    @staticmethod
    def get_article_by_slug(slug):
        try:
            return Articles\
                   .select()\
                   .where(Articles.slug == slug)\
                   .get()
        except:
            return 0

    @staticmethod
    @db.commit_on_success
    def create_article(title, body, author, draft = True):
        if len(title) > 255:
            raise ValueError("Title must be at most 255 characters")
        try:
            Articles.create(title = title,\
                            slug = slugify(title),\
                            body = body,\
                            author = author,\
                            draft = draft)
        except Exception as e:
            handle_errors("Error creating article")
            raise

    def get_previous_article(self, draft = False):
        try:
            return Articles.select()\
                   .where(Articles.draft == draft)\
                   .where(Articles.id < self.id)\
                   .order_by(Articles.id.desc())\
                   .get()
        except:
            return 0

    def get_next_article(self, draft = False):
        try:
            return Articles.select()\
                   .where(Articles.draft == draft)\
                   .where(Articles.id > self.id)\
                   .order_by(Articles.id.asc())\
                   .get()
        except:
            return 0


    @staticmethod
    @db.commit_on_success
    def update_article(article, title, body):
        if len(title) > 255:
            raise ValueError("Title must be at most 255 characters")
        try:
            article.title = title
            article.body = body
            article.date_updated = datetime.datetime.utcnow()
            article.save()
        except Exception as e:
            handle_errors("Error updating article")
            raise

    @staticmethod
    @db.commit_on_success
    def publish_article(article):
        try:
            article.draft = False
            article.save()

        except Exception as e:
            handle_errors("Error publishing article")
            raise

    @staticmethod
    @db.commit_on_success
    def delete_article(article):
        try:
            article.delete_instance()
            return 1
        except Exception as e:
            handle_errors("Error delting article")
            raise
            

    def __repr__(self):

        return "<Article: %s>" % self.title

    class Meta:
        order_by = ("-id",)
