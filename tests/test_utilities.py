from __future__ import absolute_import
from __future__ import unicode_literals

import sys
sys.path.append("..")


from main.helpers import slugify, split_filename

import unittest


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

        text = slugify("lorem     ipsum")
        self.assertEqual("lorem-ipsum", text)

        # test for tabs

        text = slugify("lorem\tipsum")
        self.assertEqual("lorem-ipsum", text)







        





if __name__ == "__main__":

    unittest.main()

