# -*- coding: utf-8 -*-
"""

    main.models.UserProjects
    ============
    
    Implements methods related to user projects view

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.


"""
from main.models.UsersModel import Users
from main.models.BaseModel import BaseModel
from main import db
from peewee import *
from datetime import datetime
from main.helpers import handle_errors


class UserProjects(BaseModel):
    
    """
    Models and methods related to projects
    """

    title = CharField(unique = True)
    body = TextField()
    date_created = DateTimeField(default = datetime.now())
    date_updated = DateTimeField(default = datetime.now())
    author = ForeignKeyField(Users, related_name = "projects")


    @staticmethod
    def get_project(id):
        """ Get project by id """
        return UserProjects.get_single("id", id)

    @staticmethod
    def get_all_projects():
        """ Returns all projects or 0 if none exist"""
        q = UserProjects.select()
        if q.count():
            return q
        return 0


    @staticmethod
    def check_exists(title, id = False):
        """ Check if project with given title exists """
        try:
           q =  UserProjects.select().where((UserProjects.title == title))
           if not id:
               return q.get()
           return q.where(UserProjects.id != id).get()
        except:
            return False


    @staticmethod
    @db.commit_on_success
    def create_project(title, body, author):
        """
        Create new project
        Arguments:
            :title (unicode) - title of the project
            :body (unicode) - body of the project
            :author (object) - object containing author info

        """
        if len(title) > 255:
            raise ValueError("Title must be at most 255 characters long")
        try:
            UserProjects.create(title = title,\
                               body = body,\
                               author = author)

        except Exception as e:
            handle_errors("error creating project")
            raise


    @staticmethod
    @db.commit_on_success
    def delete_project(project):
        """
        Delete project
        """
        try:
            project.delete_instance()
            return 1
        except Exception as e:
            handle_errors("error deleting project")
            raise
    
    @staticmethod
    @db.commit_on_success
    def update_project(project, title, body):
        """
         Update project information
         Arguments:
             :project (object) - instance of project
             :title (unicode) - new title
             :body (unicode) - new body
        """
        if len(title) > 255:
            raise ValueError("Title must be at most 255 characters long")
        try:
            project.title = title
            project.body = body
            project.date_updated = datetime.now()
            project.save()
            return 1
        except Exception as e:
            handle_errors("error updating article")
            raise

    def __repr__(self):
        return "<Project: {0}>".format(self.title)

    class Meta:
        order_by = ("-id",)
