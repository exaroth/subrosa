
import unittest
from main.models.UsersModel import Users
from playhouse.test_utils import test_database
from peewee import *

db = SqliteDatabase(":memory:")

db._flag = "db1"


class TestUsersMethods(unittest.TestCase):

    
    def test_sanity(self):

        with test_database(db, (Users,)):
            self.assertTrue(Users.table_exists())
            self.assertFalse(Users.check_any_exist())


    def test_creating_user(self):

        with test_database(db, (Users,)):
            Users.create_user(username = "konrad", password = "secret")

            self.assertTrue(Users.get_user(1))
            self.assertTrue(Users.check_exists("konrad"))
            self.assertEquals(1, Users.select().count())


            Users.create_user(username = "malgosia",\
                              password = "secret",\
                              real_name = "Malgosia Samosia", \
                              description = "test")

            self.assertEquals(2, Users.select().count())

            self.assertRaises(IntegrityError, lambda: Users.create_user(username = "konrad", password = "test2"))

    def test_utility_methods(self):

        with test_database(db, (Users,)):

            Users.create_user(username = "konrad", password = "test", real_name = "real_name")

            self.assertEquals("real_name", Users.get_user_by_username("konrad").real_name)

            konrad = Users.get_user(1)

            self.assertTrue(konrad.check_password("test"))
            self.assertFalse(konrad.check_password("wrong_password"))


if __name__ == "__main__":
    unittest.main()



