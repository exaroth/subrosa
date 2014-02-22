import os, sys
import unittest

sys.path.append("..")

from main.models import Users, BaseModel
from main import app, db



class TestUserModel(unittest.TestCase):

    def setUp(self):
        app.config["DEBUG"] = True
        db.connect()
        Users.create_table()

    def tearDown(self):
        Users.drop_table()

    def test_user_insertions(self):

        konrad = Users.create(username = "konrad",email = "exaroth@gmail.com", hash = "test", real_name = "John Doe" )

        sel = Users.select().count()
        self.assertEquals(1, sel)
        sel = Users.select().get()
        self.assertEquals("konrad", sel.username)
        self.assertEquals("exaroth@gmail.com", sel.email)

        # test for not adding required fields

    def test_required_fields(self):

        self.assertRaises(lambda: Users.create(email = "exaroth@gmail.com", hash = "test", realname = "John Doe"))

        self.assertRaises(lambda: Users.create(username = "konrad", email = "exaroth@gmail.com", real_name = "John Doe"))

        # Test for nullable real name

    def test_nullable_fields(self):

        konrad = Users.create(username = "konrad", email = "exaroth@gmail.com", hash = "test")
        sel = Users.select().get()

        self.assertEquals(None, sel.real_name)


    def test_uniqueness(self):

        user1 = Users.create(username = "konrad", email = "exaroth@gmail.com", hash = "test")

        self.assertRaises(lambda: Users.create(username = "konrad", email = "other", hash = "test"))

        self.assertRaises(lambda: Users.create(username = "other", email = "exaroth@gmail.com", hash = "test"))

    def test_multiple_user_insertions(self):

        user1 = Users.create(username = "konrad", email = "exaroth@gmail.com", hash = "test")
        user2 = Users.create(username = "malgosia", email = "malgosia@gmail.com", hash = "test")

        sel = Users.select()

        self.assertEquals(sel.count(), 2)

        self.assertEquals(sel.where(Users.username == "malgosia").get().email, "malgosia@gmail.com" )

    def test_getting_nonexistent_person_returns_false(self):

        user1 = Users.create(username = "konrad", email = "exaroth@gmail.com", hash = "test")

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
        email = "exaroth@gmail.com"
        password = "test"

        konrad = Users.create_user(username = username, email = email, password = password)
        self.assertEquals(konrad, 1)

        sel = Users.select().get()
        self.assertEquals(sel.username, "konrad")
        self.assertEquals(sel.email, "exaroth@gmail.com")
        self.assertIn("pbkdf", sel.hash)
        self.assertEquals(None, sel.real_name)

        # test for errors

        self.assertRaises(lambda: Users.create_user(username = username, email = "other", password = "other"))

    def test_getting_user_by_username(self):

        Users.create(username = "konrad", email = "exaroth@gmail.com", hash = "test")

        k = Users.get_user_by_username("konrad")

        self.assertEquals(k.username, "konrad")
        self.assertEquals(k.email, "exaroth@gmail.com")

        # test for nonexistent

        n = Users.get_user_by_username("malgosia")

        self.assertEquals(n, 0)
        self.assertFalse(n)

    def test_existence_method(self):
        Users.create(username = "konrad", email = "exaroth@gmail.com", hash = "test")

        res = Users.check_exists("konrad","exaroth@gmail.com")
        self.assertTrue(res)

        res = Users.check_exists("konrad", "nonexistent")
        self.assertTrue(res)
        res = Users.check_exists("nonexistent", "exaroth@gmail.com")
        self.assertTrue(res)

        res = Users.check_exists("nonexistent", "nonexistent")
        self.assertFalse(res)



    def test_checking_password_hash(self):

        Users.create_user("konrad", "exaroth@gmail.com", "test")

        sel = Users.select().get()

        self.assertTrue(sel.check_password("test"))
        self.assertFalse(sel.check_password("false"))




if __name__ == "__main__":
    unittest.main()


