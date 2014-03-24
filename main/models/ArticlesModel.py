# -*- coding: utf-8 -*-
"""

    main.models.ArticlesModel
    ============
    
    Implements model and methods related to subrosa articles

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.


"""

from __future__ import absolute_import

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

    title = TextField(unique = True)
    slug = TextField(unique = True)
    draft = BooleanField(default = True)
    series = TextField(null = True, default = None)
    date_created = DateTimeField(default = datetime.datetime.utcnow())
    date_updated = DateTimeField(default = datetime.datetime.utcnow())
    article_image = TextField(null = True, default = None)
    article_thumbnail = TextField(null = True, default = None)
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

    def get_article_categories(self):
        """
        Get article categories
        """

        
        return Categories.select()\
                .join(ArticleCategories)\
                .where(ArticleCategories.article == self)\
                .group_by(Categories)

    
    def save_article_categories(self, category_names, update = False):
        """
        Create Categories and ArticleCategories table if 
        category doesnt exist or article doesnt have the category yet
        """

        
        # This is lame implementation, im too stupid for this crap
        try:
            own_categories = self.get_article_categories().iterator()

            for name in category_names:
                if not Categories.select().where(Categories.name == name).exists():
                    cat = Categories.create(name = name)
                    ArticleCategories.create(article = self, category = cat)

                elif name not in [field.name for field in own_categories]:
                    cat = Categories.select().where(Categories.name == name).get()
                    ArticleCategories.create(article = self, category = cat)
        except Exception as e:
            handle_errors("error saving article categories")
            raise e



    def get_similar_articles(self, common_categories = 1, limit = 3):
        """
        Get 3 similar articles based on tag used,
        minimum 1 common tag is required
        """
        art = (ArticleCategories.select(ArticleCategories.category)\
               .join(Articles)\
               .where(ArticleCategories.article == self))

        return Articles.select(Articles, ArticleCategories)\
               .join(ArticleCategories)\
               .where((ArticleCategories.article != self) & ArticleCategories.category << art)\
               .group_by(Articles)\
               .having(fn.Count(ArticleCategories.id ) >= common_categories)\
               .order_by(fn.Count(Articles.id).desc())\
               .limit(limit)
        
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
    def create_article(title, body, author, draft = True, **kwargs):
        if len(title) > 255:
            raise ValueError("Title must be at most 255 characters")
        try:
            series = kwargs.get("series", None)        
            article_image = kwargs.get("article_image")
            article_thumbnail = kwargs.get("article_thumbnail")
            article =  Articles.create(title = title,\
                            slug = slugify(title),\
                            body = body,\
                            author = author,\
                            draft = draft,\
                            series = series,\
                            article_image = article_image,\
                            article_thumbnail = article_thumbnail
                            )
            article_categories = kwargs.get("categories", None)
            if article_categories:
                try:
                    article.save_article_categories(article_categories)
                except:
                    raise
            return article        
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
    def update_article(article, title, body, **kwargs):
        try:
            series = kwargs.get("series", None)        
            article_image = kwargs.get("article_image")
            article_thumbnail = kwargs.get("article_thumbnail")

            article.title = title
            article.body = body
            article.date_updated = datetime.datetime.utcnow()
            article.series = series
            article.article_image = article_image
            article.article_thumbnail = article_thumbnail
            article.save()
            article_categories = kwargs.get("categories", None)
            article.save_article_categories
            return article
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



class Categories(BaseModel):

    name = CharField(unique = True)

    def __repr__(self):
        return "<Category: {0}>".format(self.name)


class ArticleCategories(BaseModel):

    article = ForeignKeyField(Articles, on_delete="CASCADE", on_update="CASCADE", related_name = "articles")
    category = ForeignKeyField(Categories, on_delete="CASCADE", on_update="CASCADE", related_name = "tags")

    def __repr__(self):
        return "<Article - {0} : Category - {1}>".format(self.article, self.category)
