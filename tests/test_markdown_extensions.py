from __future__ import absolute_import
from __future__ import print_function

import sys

sys.path.append("..")

from main.markdown_ext import Markdown
import unittest


md = Markdown()




class TestMarkdownWrapper(unittest.TestCase):



    def testBasicMarkdownFunctions(self):

        md = Markdown()

        test = md("test")
        self.assertEqual("<p>test</p>", test)

        test = md("*test*")
        self.assertEqual("<p><em>test</em></p>", test)

        test = md('[test link](http://www.google.com)')
        self.assertEqual('<p><a href="http://www.google.com">test link</a></p>', test)

        test = md('![test image](http://www.kittens.com)')
        self.assertEqual('<p><img alt="test image" src="http://www.kittens.com" /></p>', test)

        test = md("1. First\n2. Second\n3. Third")

        self.assertIn("<ol>", test)

        self.assertIn("<li>First</li>", test)
        self.assertIn("<li>Second</li>", test)
        self.assertIn("<li>Third</li>", test)

    def testImageExtension(self):
        md = Markdown(extensions = ["main.md_extensions.extended_images"])

        test = md("![testing images](http://kittens.com)")

        self.assertEqual('<p><img alt="testing images" class="lazy" data-src="http://kittens.com" src="#" /></p>', test)

        test = md("[![test images](http://kittens.com)](http://puppies.com)")

        self.assertEqual('<p><a href="http://puppies.com"><img alt="test images" class="lazy" data-src="http://kittens.com" src="#" /></a></p>', test) 




if __name__ == "__main__":
    unittest.main()
