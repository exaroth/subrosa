from peewee import *

from main import app, db

from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from .helpers import handle_errors
from webhelpers.text import truncate

from slugify import slugify




class BaseModel(Model):

    class Meta:
        database = db


class Users(BaseModel):

    username = CharField( max_length = 40, unique = True, index = True )
    email = CharField(max_length = 40, unique = True )
    hash = CharField()
    real_name = CharField(max_length = 40, null = True )


    @staticmethod
    @db.commit_on_success
    def create_user(username, email, password, real_name = None):

        """ Create new user """

        try:
            return Users.create(username = username, email = email, hash = generate_password_hash(password), real_name = real_name).get_id()

        except:
            handle_errors("Error creating user")
            raise

    @staticmethod
    def check_any_exist():
        return len(list(Users.select())) > 0

    @staticmethod
    def check_exists(username, email):

        """ Check if user with given username or email already exists """

        return Users.select()\
                .where((Users.username == username) | (Users.email == email))\
                .exists()

    @staticmethod
    def get_user(id):
        try:
            return Users.select().where(Users.id == id).get()
        except:
            return 0

    @staticmethod
    def get_user_by_username(username):

        """ Get user by his username , returns 0 if not exists """

        try:
            return Users.select().where(Users.username == username).get()
        except:
            return 0

    def check_password(self, password):

        """ Compare password against the one in db """

        return check_password_hash(self.hash, password)

    def __repr__(self):
        return "<User: %s>" % self.username

    class Meta:
        order_by = ("username",)


class Articles(BaseModel):

    title = TextField(unique = True)
    slug = TextField()
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
        """ Return count of articles """
        q = Articles.select()
        if drafts:
            return q.count()
        return q.where(Articles.draft == False).count()
    
    @staticmethod
    def get_index_articles(page, per_page):
        """ Returns paginated articles for the for index """

        try:
            x =  Articles\
                    .select()\
                    .where(Articles.draft == False)\
                    .paginate(page, per_page)
            for m in x:
                print m.title
            return x
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
    @db.commit_on_success
    def create_article(title, body, author, draft):
        try:
            Articles.create(title = title, slug = slugify(title), body = body, author = author, draft = draft)
        except Exception as e:
            handle_errors("Error creating article")
            raise

    @staticmethod
    @db.commit_on_success
    def update_article(article, title, body):
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
        order_by = ("-date_created",)


class UserImages(BaseModel):

    filename = TextField(unique = True)
    showcase = TextField()
    date_added = DateTimeField(default = datetime.datetime.utcnow())
    description = TextField(null = True)
    is_vertical = IntegerField(null = True)
    gallery = BooleanField(default = False)
    external = BooleanField(default = False)
    owner = ForeignKeyField(Users, related_name = "images" )


    @staticmethod
    def get_image(id):
        try:
            return UserImages.select().where(UserImages.id == id).get()
        except:
            return 0

    @staticmethod
    def check_exists(filename):
        return UserImages.select().where(UserImages.filename == filename).exists()

    @staticmethod
    def get_count(drafts = False):
        """ Return count of images """
        return UserImages.select().count()

    @staticmethod
    def get_gallery_images(username, page, per_page, gallery = False):
        q = UserImages.select().join(Users).where(Users.username == username)
        if gallery:
            return q.where(UserImages.gallery == True).paginate(page, per_page)
        return q.paginate(page, per_page)

    @staticmethod
    @db.commit_on_success
    def gallerify(image):

        try:
            is_gallerified = image.gallery
            image.gallery = not is_gallerified
            image.save()

        except Exception as e:
            handle_errors("Error updating image")


    @staticmethod
    @db.commit_on_success
    def add_image(filename, showcase, external, description, is_vertical, owner):
        try:
            UserImages.create(
                filename = filename,
                showcase = showcase,
                external = external,
                description = description,
                is_vertical = is_vertical,
                owner = owner
            )
            return 1
        except Exception as e:
            handle_errors("Error creating image")
            raise

    @staticmethod
    @db.commit_on_success
    def delete_image(image):
        try:
            image.delete_instance()
            return 1
        except Exception as e:
            handle_errors("Error deleting image")
            raise

