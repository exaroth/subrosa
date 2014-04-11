#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from __future__ import absolute_import
from __future__ import unicode_literals

import sys
sys.path.append("..")


from subrosa.helpers import slugify, split_filename
from subrosa.models.ArticlesModel import Articles
from subrosa.models.UsersModel import Users
from subrosa.helpers import archives_generator
from playhouse.test_utils import test_database
import datetime
from peewee import *
import unittest
import time
from pprint import pprint

db = SqliteDatabase(":memory:")
db._flag = "db1"

class TestBasicHelpers(unittest.TestCase):


    def testSlugifyFunction(self):

        text = slugify("this text is a slug")

        self.assertEqual("this-text-is-a-slug", text)

        # test for no charactes

        text = slugify("")
        self.assertEqual("", text)

        # text for non-ascii characters  characters

        text = slugify("grzęgżóką")
        self.assertEqual("grzegzoka", text)

        # text for more than one space

        text = slugify(u"lorem     ipsum")
        self.assertEqual("lorem-ipsum", text)

        # test for tabs

        text = slugify("lorem\tipsum")
        self.assertEqual("lorem-ipsum", text)




if __name__ == "__main__":

    unittest.main()

