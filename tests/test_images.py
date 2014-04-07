import unittest
from subrosa.models.UsersModel import Users
from subrosa.models.UserImagesModel import UserImages
from playhouse.test_utils import test_database
from peewee import *

db = SqliteDatabase(":memory:")

db._flag = "db1"


class TestImagesMethods(unittest.TestCase):
    

    ADDRESS = "http://www.imgur.com/kitten.jpg"

    def test_creating_and_deleting_image(self):
        
        with test_database(db, (Users, UserImages)):
            Users.create_user(username = "konrad", password = "test")
            user1 = Users.select().get()

            UserImages.add_image(image_link = self.ADDRESS,\
                                description = "test",\
                                is_vertical = True, \
                                owner = user1,\
                                imgur_img = False,\
                                delete_hash = None)


            image = UserImages.select().get()

            self.assertEquals(self.ADDRESS ,image.image_link)
            self.assertEquals("test", image.description)
            self.assertEquals(user1, image.owner)

            UserImages.add_image(image_link = self.ADDRESS,\
                                description = "test",\
                                is_vertical = True, \
                                owner = user1,\
                                imgur_img = False,\
                                delete_hash = None)

            self.assertEquals(2, UserImages.get_count())

            self.assertTrue(UserImages.check_exists(self.ADDRESS))
            self.assertFalse(UserImages.check_exists(self.ADDRESS + "bam"))
            image = UserImages.get_image(2)
            UserImages.delete_image(image)
            self.assertEquals(1, UserImages.get_count())
            image = UserImages.get_image(1)
            UserImages.delete_image(image)
            self.assertEquals(0, UserImages.get_count())

    def test_test_gallery_methods(self):

        with test_database(db, (Users, UserImages)):
            Users.create_user(username = "konrad", password = "test")
            user1 = Users.select().get()

            UserImages.add_image(image_link = self.ADDRESS,\
                                description = "test",\
                                is_vertical = True, \
                                owner = user1,\
                                imgur_img = False,\
                                delete_hash = None)

            
            image = UserImages.select().get()
            self.assertFalse(image.gallery)
            UserImages.gallerify(image)
            self.assertTrue(image.gallery)
            UserImages.gallerify(image)
            self.assertFalse(image.gallery)

            for num in range(2, 10):
                UserImages.add_image(image_link = "test image %d" % num,\
                                    description = "test %d" % num,\
                                    owner = user1)

            self.assertEquals(9, UserImages.get_count())

            paginated = UserImages.get_gallery_images(1, 2)

            self.assertEquals(2, len(tuple(paginated)))

            self.assertIn(self.ADDRESS, str(tuple(paginated)))
            self.assertNotIn("test image 3", str(tuple(paginated)))

            paginated = UserImages.get_gallery_images(5, 2)

            self.assertIn("test image 9", str(tuple(paginated)))
            self.assertEquals(1, len(tuple(paginated)))



if __name__ == "__main__":
    unittest.main()




