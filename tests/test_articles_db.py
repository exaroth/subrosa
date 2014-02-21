import unittest
import os, sys

sys.path.append("..")

from main.models_p import Users, Articles, db
from main import app



class TestArticlesModel(unittest.TestCase):

    def setUp(self):

        app.config["DEBUG"] = False
        db.connect()
        Users.create_table()
        Articles.create_table()

    def tearDown(self):

        Users.drop_table()
        Articles.drop_table()



