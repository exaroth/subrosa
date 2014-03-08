#!/usr/bin/env python
from main import db, app
from main.models.ArticlesModel import Articles
from main.models.UserImagesModel import UserImages
from main.models.UsersModel import Users
from main.models.UserProjectsModel import UserProjects


db.connect()


app.config["DEBUG"] = False

try:
    Users.create_table()
    Articles.create_table()
    UserImages.create_table()
    UserProjects.create_table()
    print "Database created"
except:
    pass


