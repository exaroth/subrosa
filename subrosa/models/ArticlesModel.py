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

from subrosa import db
from subrosa.helpers import handle_errors, slugify
from subrosa.models.BaseModel import BaseModel
from subrosa.models.UsersModel import Users




class Articles(BaseModel):

    """
    Models and methods related to articles
    """

    title = TextField(unique = True)
    slug = TextField(unique = True, index = True)
    draft = BooleanField(default = True)
    series = TextField(null = True, default = None)
    date_created = DateTimeField(default = datetime.datetime.utcnow())
    date_updated = DateTimeField(default = datetime.datetime.utcnow())
    article_image = TextField(null = True, default = None)
    article_thumbnail = TextField(null = True, default = None)
    body = TextField()
    author = ForeignKeyField(Users, related_name = "article")


    @staticmethod
    def get_article(id):
        return Articles.get_single("id", id)


    @staticmethod
    def get_article_by_slug(slug):
        """ Get article by it\'s slug """

        return Articles.get_single("slug", slug)

    @staticmethod
    def get_count(drafts = False):
        """
        Return number of articles 
        Arguments:
            :drafts (bool) - if True includes drafts in result
        """
        q = Articles.select()
        if drafts:
            return q.count()
        return q.where(Articles.draft == False).count()
    
    @staticmethod
    def get_index_articles(page, per_page):
        """
        Returns paginated articles for the index page
        Arguments:
            :page - current page
            :per_page - number of articles to be displayed per page
        """

        try:
            return Articles\
                    .select()\
                    .where(Articles.draft == False)\
                    .paginate(page, per_page)
        except:
            handle_errors("Error getting articles")

    @staticmethod
    def get_user_articles(username):

        """
        Get all articles belonging to user
        Arguments:
            :username - username of articles' author
        """

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
        Arguments:
            :title - title of the article
            :id - (bool)
        """

        try:
           q =  Articles.select().where((Articles.title == title))
           if not id:
               return q.get()
           return q.where(Articles.id != id).get()
        except:
            return False

    def get_article_series(self):
        """ Return all articles belonging to series"""
        if not self.series.strip():
            return 0

        q = Articles.select().where(Articles.series == self.series)     
        if not q.count():
            return 0
        return q     

    def get_article_categories(self):

        """
        Returns all articles' categories
        """
        
        return Categories.select()\
                .join(ArticleCategories)\
                .where(ArticleCategories.article == self)\
                .group_by(Categories)

    
    def save_article_categories(self, category_names, update = False):

        """

        Create Categories and ArticleCategories table if 
        category doesn\'t exist or article doesn\'t have the category yet
        Arguments:
            : category_names (list/tuple) - iterable containing categories' names
            : update (bool) - if True performs a check whether user has deleted any categories
                             
        """

        
        if not category_names:
            return

        try:
            new_categories = set(category_names)
            own_categories = self.get_article_categories().iterator()

            for name in new_categories:
                if not Categories.select().where(Categories.name == name).exists():
                    cat = Categories.create(name = name)
                    ArticleCategories.create(article = self, category = cat)

            existing_categories = set([field.name for field in own_categories])
            to_add = list(new_categories.difference(existing_categories))
            for name in to_add:
                cat = Categories.select().where(Categories.name == name).get()
                ArticleCategories.create(article = self, category = cat)
            if update:
                q = list(existing_categories.difference(new_categories))
                if q:
                    to_remove = Categories.select().where(Categories.name << q)
                    delete_query = ArticleCategories.delete()\
                                   .where((ArticleCategories.article == self)\
                                   & (ArticleCategories.category << to_remove)) 
                    delete_query.execute()

        except Exception as e:
            handle_errors("error saving article categories")
            raise e



    def get_similar_articles(self, common_categories = 1, limit = 3):
        """
        Get 3 similar articles based on tag used,
        minimum 1 common tag is required
        Arguments:
            :common_categories (int) - minimum number of common categories
            :limit (int) - number of articles to be returned
        """
        art = (ArticleCategories.select(ArticleCategories.category)\
               .join(Articles)\
               .where(ArticleCategories.article == self))

        return Articles.select()\
               .join(ArticleCategories, JOIN_LEFT_OUTER)\
               .where((ArticleCategories.article != self) & ArticleCategories.category << art)\
               .group_by(Articles)\
               .having(fn.Count(ArticleCategories.id ) >= common_categories)\
               .order_by(fn.Count(Articles.id).desc())\
               .limit(limit)
        

    @staticmethod
    @db.commit_on_success
    def create_article(title, body, author, draft = True, **kwargs):
        
        """
        Creates new article
        Returns instance of the created article

        Arguments:
            :title  (string/unicode)(required) - title of the article
            :body   (string/unicode)(required) - body of the article
            :author (object) - Users object containing author\'s info
            :draft  (bool) (optional)- whether article is published
            :categories (list/tuple) (optional) - list containing
            names of article categories
            :series (string/unicode) (optional) - article series
            :article_image (string) - url to be used as title
            image for article
            :article_thumbnail (string) - url for articles thumbnail
        """


        if len(title) > 255:
            raise ValueError("Title must be at most 255 characters")
        try:
            series = kwargs.get("series", None)        
            article_image = kwargs.get("article_image", None)
            article_thumbnail = kwargs.get("article_thumbnail", None)
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

    @staticmethod
    @db.commit_on_success
    def update_article(article, title, body, **kwargs):
        """
        Updates an article
        Arguments:
            :article (object) - instance of the article to be updated
            :title  (string/unicode)(required) - title of the article
            :body   (string/unicode)(required) - body of the article
            :categories (list/tuple) (optional) - list containing
            names of article categories
            :series (string/unicode) (optional) - article series
            :article_image (string) - url to be used as title
            image for article
            :article_thumbnail (string) - url for articles thumbnail
        """

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
            article.save_article_categories(article_categories, True)
            return article
        except Exception as e:
            handle_errors("Error updating article")
            raise

    def get_previous_article(self, draft = False):

        """
        Return previous article or 0 if doesn't exist
        Arguments:
            :draft (bool)(default: False) - whether to include drafts 
        """

        try:
            return Articles.select()\
                   .where(Articles.draft == draft)\
                   .where(Articles.id < self.id)\
                   .order_by(Articles.id.desc())\
                   .get()
        except:
            return 0

    def get_next_article(self, draft = False):

        """
        Return next article or 0 if doesn't exist
        Arguments:
            :draft (bool)(default: False) - whether to include drafts 
        """

        try:
            return Articles.select()\
                   .where(Articles.draft == draft)\
                   .where(Articles.id > self.id)\
                   .order_by(Articles.id.asc())\
                   .get()
        except:
            return 0


    @db.commit_on_success
    def publish_article(self):
        """Reverses 'draft' status of the article"""
        try:
            self.draft = not self.draft
            self.save()

        except Exception as e:
            handle_errors("Error publishing article")
            raise

    @db.commit_on_success
    def delete_article(self):
        """ Deletes an article"""
        try:
            self.delete_instance()
            return 1
        except Exception as e:
            handle_errors("Error deleting article")
            raise
            

    def __repr__(self):

        return "<Article: {0}>".format(self.title)

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
