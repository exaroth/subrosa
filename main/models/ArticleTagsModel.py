from __future__ import absolute_import


from main.models.ArticlesModel import Articles
from main.models.BaseModel import BaseModel
from peewee import *
from main import db


class Tags(BaseModel):

    name = CharField(unique = True)


class ArticleTags(BaseModel):

    article = ForeignKeyField(Articles, related_name = "articles")
    tag = ForeignKeyField(Tags, related_name = "tags")

