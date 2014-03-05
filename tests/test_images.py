import unittest

import os, sys

sys.path.append("..")

from main.models.UserImagesModel import UserImages
from main.models.UsersModel import Users
from main import app, db

class TestImagesMethods(unittest.TestCase):

    def setUp(self):
        app.config["DEBUG"] = True
        db.connect()
        Users.create_table()
        UserImages.create_table()

    def tearDown(self):
        Users.drop_table()
        UserImages.drop_table()

    
    def test_adding_image(self):

        Users.create_user(username = "konrad", email = "exaroth", password = "test")
        k = Users.select().get()
        UserImages.add_image(image_link = "test",
                            description = "test",
                            is_vertical = False,
                            owner = k)

        sel = UserImages.select().get()

        self.assertEquals(sel.image_link, "test")
        self.assertEquals(sel.owner.username, "konrad")




if __name__ == "__main__":

    unittest.main()


