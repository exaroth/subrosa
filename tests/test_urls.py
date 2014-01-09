import os, sys
import nose, unittest
from flask.ext.testing import TestCase
from bs4 import BeautifulSoup as bs
import tempfile
import flask

sys.path.append(os.getcwd())
sys.path.append("..")

from main import app, db
from main.models import User, Articles

class BasicTest(TestCase):

    """
    Base setup for testing flask application:

        - Creates temporary database in current folder
        - Sets up flask test client
        - Defines some basic utility functions used for testing
        - Database is destroyed after each test
    """

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + tempfile.mkstemp(dir = ".")[1]
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.unlink(app.config["SQLALCHEMY_DATABASE_URI"][10:])

    def add_user(self, username, email, password):
        test_user = User(username = username, email = email, password = password)
        db.session.add(test_user)
        db.session.commit()
        return test_user

    def add_article(self, title, body, author):
        test_article = Articles(title = title, body = body, author = author)
        db.session.add(test_article)
        db.session.commit()
        return test_article

    def get_element(self, haystack, needle):
        """
         finds all the occurencies of the element in a body
         and returns a list containing all of them
        """
        temp = bs(haystack)
        return temp.find_all(needle)

    def login(self, username, password):
        return self.client.post("/admin", data = dict(
            username = username,
            password = password
        ), follow_redirects = True)

    def logout(self):
        return self.client.get("/logout", follow_redirects = True)

class TestBasicSiteFunctionality(BasicTest):

    def setUp(self):
        super(TestBasicSiteFunctionality, self).setUp()
        self.test_user = self.add_user("test", "example@example.com", "test")


    def testIndex(self):

        # Sanity tests

        rv = self.client.get("/")
        self.assertIn("Main Content", rv.data)
        self.assertIn("No articles here yet", rv.data)
        rv = self.login("test", "test")
        article_body = "test body"
        article = self.add_article("test title", "test body", self.test_user)
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("test title", rv.data)
        self.assertNotIn("No articles here yet", rv.data)
        self.assertContext("title", "Main Content")

    def testLogin(self):

        # Test correct credentials

        rv = self.client.post("/admin", data = dict(username = "test", password = "test"), follow_redirects = True )
        self.assertIn("Hello test!", rv.data)
        self.assert200(rv)
        self.add_article(title = "test title", body = "test body", author = self.test_user)
        rv = self.login("test", "test")
        self.assertIn("test title", rv.data)
        self.assertIn("Hello test", rv.data)
        self.logout()

        # Test incorrect credentials
        
        # Test Empty

        rv = self.login("", "")
        self.assertIn("Error", rv.data)

        # Test incorrect username

        rv = self.login("wrong_user", "test")
        self.assertIn("Error", rv.data)

        # Test incorrect password

        rv = self.login("test", "wrong_password")
        self.assertIn("Error", rv.data)

    def testAddingArticles(self):

        # Test unauthorized users cannot create articles

        rv = self.client.get("/create_article", follow_redirects = True)
        self.assertIn("Main Content", rv.data)

        # Test creating and article

        self.login("test", "test")
        rv = self.client.get("/create_article")
        self.assert200(rv)
        self.assertIn("Create new article", rv.data)
        rv = self.client.post("/create_article", data = dict(title = "test title", body = "test body"), follow_redirects = True)
        self.assertIn("test title", rv.data)
        self.assertIn("test body", rv.data)

        # Test that error is raised when body or title are empty

        rv = self.client.post("/create_article", data = dict(title = "", body = "test body"), follow_redirects = True)
        self.assertIn("Error", rv.data)


        rv = self.client.post("/create_article", data = dict(title = "sample title", body = ""), follow_redirects = True)
        self.assertIn("Error", rv.data)

        # Test articles are properly added to db

        article = Articles.query.first()

        self.assertEquals("test title", article.title)
        self.assertEquals("test body", article.body)
        self.assertEquals("test", article.author.username)

        # Test that two articles cant have same title

        rv = self.client.post("/create_article", data = dict(title = "test title", body = "test body"), follow_redirects = True)
        self.assertIn("Error", rv.data)

        rv = self.client.get("/")
        articles = self.get_element(rv.data, "article")
        self.assertEquals(len(articles), 1)

        self.add_article("article 2", "body 2", self.test_user)
        article = Articles.query.get(2)
        self.assertEquals(article.title, "article 2")
        self.assertEquals(article.body, "body 2")
        self.assertEquals(article.author.username, "test")

        rv = self.client.get("/")
        articles = self.get_element(rv.data, "article")
        self.assertEquals(len(articles), 2)

    def testDeletingArticles(self):

        self.add_article("test title", "test body", self.test_user)
        self.add_article("someothertitle", "someotherbody", self.test_user)

        # Test no unauthorized users can delete articles

        rv = self.client.get("/delete_article/1")
        self.assertRedirects(rv, "/")
        rv = self.client.get("/")
        elems = self.get_element(rv.data, "article")
        self.assertEquals(len(elems), 2)
    
        # Test that only author of the article can delete it
        
        self.add_user("test2", "example2@gmail.com", "somestupidpassword")
        self.login("test2", "somestupidpassword")
        rv = self.client.get("/delete_article/1")
        self.assertRedirects(rv, "/")
        rv = self.client.get("/")
        elems = self.get_element(rv.data, "article")
        self.assertEquals(len(elems), 2)

        self.logout()

        # Test deleting articles as owner

        self.login("test", "test")

        rv = self.client.get("/delete_article/1", follow_redirects = True)
        self.assert200(rv)
        self.assertNotIn("test title", rv.data)
        elems = self.get_element(rv.data, "article")
        self.assertEquals(len(elems), 1)
        articles = Articles.query.all()
        self.assertEquals(len(articles), 1)
        rv = self.client.get("/delete_article/1")
        self.assertIn("Page not found", rv.data)

    def testUpdatingArticles(self):

        self.add_article("test title", "test body", self.test_user)
        self.add_article("someothertitle", "someotherbody", self.test_user)

        
        # Test edit_article needs an argument

        rv = self.client.get("/edit")
        self.assertIn("Page not found", rv.data)

        # Test no unauthorized users can delete articles

        rv = self.client.get("/edit/1")
        self.assertRedirects(rv, "/")
        rv = self.client.get("/edit/1")
        self.assertRedirects(rv, "/")
        rv = self.client.get("/edit/1", data = dict(title = "dummy", body = "dummy"))
        self.assertRedirects(rv, "/")

        # Test no users beside author can edit articles

        self.add_user("dummy_user", "dummy@dummy.com", "dummy")
        self.login("dummy_user", "dummy")

        rv = self.client.get("/edit/1")
        self.assertRedirects(rv, "/")
        rv = self.client.get("/edit/1")
        self.assertRedirects(rv, "/")
        rv = self.client.get("/edit/1", data = dict(title = "dummy", body = "dummy"))
        self.assertRedirects(rv, "/")

        self.logout()

        # Test updating articles as owner

        self.login("test", "test")

        rv = self.client.get("/edit/1")
        self.assert200(rv)
        self.assertIn("Edit article",rv.data)
        self.assertIn("test title", rv.data)

        rv = self.client.post("/edit/1", data = dict(title = "updated title", body = "updated body"), follow_redirects = True)
        self.assertIn("updated title", rv.data)
        self.assertIn("updated body", rv.data)
        self.assertIn("Hello test!", rv.data)

        new_article = Articles.query.all()[0]
        self.assertEquals(new_article.title, "updated title")
        self.assertEquals(new_article.body, "updated body")

        # Test that the user cant submit article with empty title or body

        rv = self.client.post("/edit/1", data = dict(title = "", body = "some body"), follow_redirects = True)
        self.assertIn("Error", rv.data)
        rv = self.client.post("/edit/1", data = dict(title = "some title", body = ""), follow_redirects = True)
        self.assertIn("Error", rv.data)

        # Test that when updating article its title cant have same title as other article

        rv = self.client.post("/edit/1", data = dict(title = "someothertitle", body = "some body"), follow_redirects = True)
        self.assertIn("Error", rv.data)

        # But it can have its title unchanged

        rv = self.client.post("/edit/1", data = dict(title = "test title", body = "changed body"), follow_redirects = True)
        self.assertIn("Hello test!", rv.data)
        self.assertIn("changed body", rv.data)


if __name__ == "__main__":

    unittest.main()
