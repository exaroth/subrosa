import os, sys
import unittest

sys.path.append("..")

from main.models.UsersModel import Users
from main import app, db



class TestUserModel(unittest.TestCase):

    def setUp(self):
        app.config["DEBUG"] = True
        db.connect()
        Users.create_table()

    def tearDown(self):
        Users.drop_table()

    def test_user_insertions(self):

        konrad = Users.create(username = "konrad", hash = "test", real_name = "John Doe" )

        sel = Users.select().count()
        self.assertEquals(1, sel)
        sel = Users.select().get()
        self.assertEquals("konrad", sel.username)

        # test for not adding required fields

    def test_required_fields(self):

        self.assertRaises(lambda: Users.create( hash = "test", realname = "John Doe"))

        self.assertRaises(lambda: Users.create(username = "konrad", real_name = "John Doe"))

        # Test for nullable real name

    def test_nullable_fields(self):

        konrad = Users.create(username = "konrad", hash = "test")
        sel = Users.select().get()

        self.assertEquals(None, sel.real_name)


    def test_uniqueness(self):

        user1 = Users.create(username = "konrad", hash = "test")

        self.assertRaises(lambda: Users.create(username = "konrad", hash = "test"))

        self.assertRaises(lambda: Users.create(username = "other", hash = "test"))

    def test_multiple_user_insertions(self):

        user1 = Users.create(username = "konrad", hash = "test")
        user2 = Users.create(username = "malgosia", hash = "test")

        sel = Users.select()

        self.assertEquals(sel.count(), 2)

        self.assertEquals(sel.where(Users.username == "malgosia").get().username, "malgosia" )

    def test_getting_nonexistent_person_returns_false(self):

        user1 = Users.create(username = "konrad", hash = "test")

        # if user doesnt exists raises an error
        self.assertRaises(lambda: Users.select().where(Users.username == "malgosia").get())


class TestUserMethods(unittest.TestCase):

    def setUp(self):
        app.config["DEBUG"] = True
        db.connect()
        Users.create_table()

    def tearDown(self):
        Users.drop_table()

    
    def test_inserting_users(self):

        username = "konrad"
        password = "test"

        konrad = Users.create_user(username = username, password = password)
        self.assertEquals(konrad, 1)

        sel = Users.select().get()
        self.assertEquals(sel.username, "konrad")
        self.assertIn("pbkdf", sel.hash)
        self.assertEquals(None, sel.real_name)

        # test for errors

        self.assertRaises(lambda: Users.create_user(username = username, password = "other"))

    def test_getting_user_by_username(self):

        Users.create(username = "konrad", hash = "test")

        k = Users.get_user_by_username("konrad")

        self.assertEquals(k.username, "konrad")

        # test for nonexistent

        n = Users.get_user_by_username("malgosia")

        self.assertEquals(n, 0)
        self.assertFalse(n)

    def test_existence_method(self):
        Users.create(username = "konrad", hash = "test")

        res = Users.check_exists("konrad")
        self.assertTrue(res)

        res = Users.check_exists("konrad")
        self.assertTrue(res)
        res = Users.check_exists("nonexistent")
        self.assertFalse(res)

        res = Users.check_exists("nonexistent")
        self.assertFalse(res)



    def test_checking_password_hash(self):

        Users.create_user("konrad", "test")

        sel = Users.select().get()

        self.assertTrue(sel.check_password("test"))
        self.assertFalse(sel.check_password("false"))




if __name__ == "__main__":
    unittest.main()


