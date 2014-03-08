import unittest
from main.models.UsersModel import Users
from main.models.UserProjectsModel import UserProjects
from playhouse.test_utils import test_database
from peewee import *

db = SqliteDatabase(":memory:")

db._flag = "db1"


class TestProjectsMethods(unittest.TestCase):

    def test_creating_project(self):

        with test_database(db, (Users, UserProjects)):

            user1 = Users.create_user("konrad", "test")

            UserProjects.create_project(title = "test project", body = "test", author = user1)
            
            project = UserProjects.select().get()
            self.assertTrue(project)

            self.assertEquals("test project", project.title)
            self.assertEquals("konrad", project.author.username)

            UserProjects.create_project(title = "test project 2", body = "test", author = user1)
            self.assertTrue(UserProjects.check_exists("test project 2"))
            
            q = UserProjects.select()

            self.assertEquals(2, q.count())

            self.assertRaises(IntegrityError, lambda: UserProjects.create_project(title = "test project", body = "test", author = user1))


    def test_deleting_adn_updating_projects(self):

        with test_database(db, (Users, UserProjects)):

            user1 = Users.create_user("konrad", "test")
            UserProjects.create_project(title = "test project", body = "test", author = user1)

            project = UserProjects.get_project(1)
            UserProjects.update_project(project, "changed", "changed")
            project = UserProjects.get_project(1)
            self.assertEquals("changed", project.title)
            self.assertEquals("changed", project.body)

            UserProjects.delete_project(project)

            self.assertEquals(0, UserProjects.select().count())
