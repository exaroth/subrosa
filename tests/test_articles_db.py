import unittest
import os, sys

sys.path.append("..")

from main.models.ArticlesModel import Articles
from main.models.UsersModel import Users
from main import app, db
import time
import datetime



class TestArticlesModel(unittest.TestCase):

    def setUp(self):

        app.config["TESTING"] = True
        db.connect()
        Users.create_table()
        Articles.create_table()
        Users.create(username = "konrad", hash = "test")

    def tearDown(self):

        Users.drop_table()
        Articles.drop_table()


    def test_creating_article(self):


        k = Users.select().get()

        Articles.create(title = "test articles", slug = "test-article", body = "testing testing...", author = k)

        article = Articles.select().get()

        self.assertEquals("test articles", article.title)
        self.assertEquals(article.draft, True)

        self.assertEquals(article.body, "testing testing...")

    def test_updating_article(self):


        k = Users.select().get()

        Articles.create(title = "test articles", slug = "test-article", body = "testing testing...", author = k)

        article = Articles.select().get()

        article.draft = False
        article.save()

        article = Articles.select().get()

        self.assertEquals(article.draft, False)

    def test_multiple_articles(self):
        k = Users.select().get()
        Articles.create(title = "test articles", slug = "test-article", body = "testing testing...", author = k, date_created = datetime.datetime(2010, 1, 1,1, 10, 10))
        Articles.create(title = "test articles2", slug = "test-article2", body = "testing testing...", author = k, date_created = datetime.datetime(2013, 1, 2, 3, 4, 5))
        articles = Articles.select()
        self.assertEquals(2, articles.count())

        self.assertTrue(articles.where(Articles.title == "test articles2").exists())

        # ordering

        articles = Articles.select()

        self.assertEquals("test articles2", articles[0].title)

class TestArticlesMethods(unittest.TestCase):

    def setUp(self):

        app.config["DEBUG"] = False
        db.connect()
        Users.create_table()
        Articles.create_table()
        Users.create(username = "konrad", hash = "test")

    def tearDown(self):

        Users.drop_table()
        Articles.drop_table()

    def test_getting_article_count(self):

        k = Users.select().get()

        Articles.create( title = "test article 1", slug = "test-article-1", body = "testing", author = k )
        Articles.create( title = "test article 2", slug = "test-article-2", body = "testing", author = k )
        Articles.create( title = "test article 3", slug = "test-article-3", body = "testing", author = k )

        c = Articles.get_count( drafts = True )
        self.assertEquals(c, 3)

        upd = Articles.select().get()
        upd.draft = False
        upd.save()
        c = Articles.get_count(drafts = False)
        self.assertEquals(1, c)

    def test_getting_index_articles(self):

        k = Users.select().get()

        Articles.create( title = "test article 1", slug = "test-article-1", body = "testing", author = k, draft = False )
        Articles.create( title = "test article 2", slug = "test-article-2", body = "testing", author = k, draft = False )
        Articles.create( title = "test article 3", slug = "test-article-3", body = "testing", author = k, draft = False )
        Articles.create( title = "test article 4", slug = "test-article-4", body = "testing", author = k, draft = False )

        x = Articles.get_index_articles(1, 3)

        self.assertIn("test article 1", str(list(x)))
        self.assertNotIn("test article 4>", str(list(x)))

        self.assertEquals(3, len(list(x)))

        x = Articles.get_index_articles(2, 3)

        self.assertNotIn("test article 1", str(list(x)))
        self.assertIn("test article 4", str(list(x)))

        self.assertEquals(1, len(list(x)))

        x = Articles.get_index_articles(3, 3)

        self.assertFalse(tuple(x))

    def test_getting_user_articles(self):
        k = Users.select().get()
        Users.create(username = "malgosia", hash = "test")
        m = Users.select().where(Users.username == "malgosia").get()

        Articles.create( title = "test article 1", slug = "test-article-1", body = "testing", author = k, draft = False )
        Articles.create( title = "test article 2", slug = "test-article-2", body = "testing", author = k, draft = False )
        Articles.create( title = "test article 3", slug = "test-article-3", body = "testing", author = k, draft = False )
        Articles.create( title = "test article 4", slug = "test-article-4", body = "testing", author = k, draft = False )
        Articles.create( title = "test article 5", slug = "test-article-5", body = "testing", author = m, draft = False )

        articles = Articles.get_user_articles("konrad")

        self.assertIn("test article 1", str(list(articles)))
        self.assertIn("test article 4", str(list(articles)))
        self.assertNotIn("test article 5", str(list(articles)))

        articles = Articles.get_user_articles("malgosia")
        self.assertIn("test article 5", str(list(articles)))

    def test_existence_method(self):
        k = Users.select().get()
        Articles.create( title = "test article 1", slug = "test-article-1", body = "testing", author = k, draft = False )
        Articles.create( title = "test article 2", slug = "test-article-2", body = "testing", author = k, draft = False )
        Articles.create( title = "test article 3", slug = "test-article-3", body = "testing", author = k, draft = False )
        Articles.create( title = "test article 4", slug = "test-article-4", body = "testing", author = k, draft = False )

        self.assertTrue(Articles.check_exists("test article 1"))
        self.assertFalse(Articles.check_exists("nonexistent"))

        self.assertFalse(Articles.check_exists("test article 1", 1))
        self.assertTrue(Articles.check_exists("test article 1", 2))

    def test_creating_articles(self):
        k = Users.select().get()

        Articles.create_article(title = "test", body = "test", author = k, draft = False)

        a = Articles.select().get()
        self.assertEquals("test", a.title)
        self.assertEquals("konrad", a.author.username)
        self.assertEquals("test", a.slug)

        Articles.create_article(title = "test2", body = "test2", author = k, draft = True)

        self.assertEquals(2, Articles.select().count())
        self.assertIn("test2", str(list(Articles.select())))

    def test_updating_article(self):

        k = Users.select().get()

        Articles.create(title = "test", slug = "test", body = "test", author = k, draft = True)


        a = Articles.select().get()

        Articles.update_article(a, "zmieniony", "zmieniony")


        a = Articles.select().get()
        self.assertEquals("zmieniony", a.title)
        self.assertEquals("zmieniony", a.body)


    def test_deleting_articles(self):
        k = Users.select().get()

        Articles.create(title = "test", slug = "test", body = "test", author = k, draft = True)

        a = Articles.select().get()

        res = Articles.delete_article(a)
        self.assertEquals(1, res)
        sel = Articles.select().count()

        self.assertFalse(sel)




if __name__ == "__main__":

    unittest.main()




