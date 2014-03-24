#!/usr/bin/env python

from __future__ import print_function

from main import db, app
from main.models.ArticlesModel import Articles, Categories, ArticleCategories
from main.models.UserImagesModel import UserImages
from main.models.UsersModel import Users
from main.models.UserProjectsModel import UserProjects
from main.models.ConfigModel import ConfigModel


db.connect()


app.config["DEBUG"] = False

try:
    for field in (Users, Articles, UserImages, UserProjects, ConfigModel, Categories, ArticleCategories):
        if not field.table_exists():
            field.create_table()
        else:
            print("Table already exists")

    print ("Tables created")

except:
    raise Exception("Error occured when creating tables, check your database configuration")


