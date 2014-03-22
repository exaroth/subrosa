from __future__ import absolute_import

import sys

sys.path.append("..")

import unittest
from main.models.UsersModel import Users
from main.models.ArticlesModel import Articles, Categories, ArticleCategories
from playhouse.test_utils import test_database
from peewee import *

db = SqliteDatabase(":memory:")

db._flag = "db1"


class TestArticlesMethods(unittest.TestCase):


    def test_creating_article(self):

        with test_database(db, (Users, Articles)):
            user1 = Users.create_user(username = "konrad", password = "test")
            article = Articles.create_article(title = "test",\
                                    body = "test",\
                                    draft = True,\
                                    author = user1)

            self.assertEquals("test", article.title)
            self.assertEquals("konrad",article.author.username)

            Articles.create_article(title = "test2",\
                                   body = "test",\
                                   draft = False, \
                                   author = user1)

            self.assertRaises(IntegrityError,\
                              lambda: Articles.create_article(title = "test",\
                                                              body = "test",\
                                                              author = user1))

            articles = Articles.get_user_articles("konrad")

            self.assertEquals(2,len(tuple(articles)))

            user2 = Users.create_user(username = "malgosia", password = "test")
            Articles.create_article(title = "test3", \
                                   body = "test",\
                                   author = user2)

            articles = Articles.get_user_articles("konrad")
            self.assertEquals(2,len(tuple(articles)))
            articles2 = Articles.get_user_articles("malgosia")
            self.assertEquals(1,len(tuple(articles2)))

    def test_getting_article_info(self):

        with test_database(db, (Users, Articles)):
            user1 = Users.create_user(username = "konrad", password = "test")
            article = Articles.create_article(title = "test article 1", \
                                    body = "test",
                                    author = user1)

            self.assertEquals("test-article-1", article.slug)
            self.assertEquals(article, Articles.get_article_by_slug("test-article-1"))
            article2 = Articles.create_article(title = "test article 2", body = "test", author = user1)
            self.assertEquals(article2, article.get_next_article(True))
            self.assertEquals(0,article.get_previous_article())
            self.assertEquals(article, article2.get_previous_article(True))
            self.assertEquals(0, article2.get_next_article())

            article3 = Articles.create_article(title = "test article 3",\
                                    body = "test",\
                                    draft = False,\
                                    author = user1)

            self.assertEquals(1, Articles.get_count(drafts = False))
            self.assertEquals(3, Articles.get_count(drafts = True))
            self.assertTrue(Articles.check_exists("test article 1"))
            self.assertFalse(Articles.check_exists("nonexistent"))

            for x in range(4,10):
                title = "test article %d" % x
                Articles.create_article(title = title, body = "test", author = user1, draft = False)

            self.assertEquals(9, Articles.get_count(True))

            paginated = Articles.get_index_articles(3, 3)

            self.assertEquals(7, paginated.wrapped_count())

            self.assertIn("test article 3", str(tuple(paginated)))
            self.assertNotIn("test article 1", str(tuple(paginated)))
            self.assertNotIn("test article 9", str(tuple(paginated)))

            paginated = Articles.get_index_articles(1, 3)

            self.assertIn("test article 9", str(tuple(paginated)))
            self.assertIn("test article 7", str(tuple(paginated)))

    def test_misc_article_methods(self):

        with test_database(db, (Users, Articles)):
            user1 = Users.create_user(username = "konrad", password = "test")
            article = Articles.create_article(title = "test article", body = "test", draft = True, author = user1)

            Articles.update_article(article, title = "changed", body = "changed")
            self.assertEquals("changed", article.title)
            self.assertEquals("changed", article.body)

            Articles.publish_article(article)
            self.assertFalse(article.draft)

            Articles.delete_article(article)
            self.assertEquals(0, Articles.get_count(True))

    def test_getting_similar_articles(self):

        with test_database(db, (Users, Articles, Categories, ArticleCategories)):
            Users.create_user(username = "konrad", password = "test")
            user1 = Users.select().get()

            article1 = Articles.create_article(title = "test article1", body = "test", draft = True, author = user1)
            article2 = Articles.create_article(title = "test article2", body = "test", draft = True, author = user1)
            article3 = Articles.create_article(title = "test article3", body = "test", draft = True, author = user1)
            article4 = Articles.create_article(title = "test article4", body = "test", draft = True, author = user1)
            article5 = Articles.create_article(title = "test article5", body = "test", draft = True, author = user1)
            article6 = Articles.create_article(title = "test article6", body = "test", draft = True, author = user1)
            article7 = Articles.create_article(title = "test article7", body = "test", draft = True, author = user1)

            category1 = Categories.create(name = "test1")
            category2 = Categories.create(name = "test2")
            category3 = Categories.create(name = "test3")
            category4 = Categories.create(name = "test4")

            ArticleCategories.create(article = article1, category = category1)
            ArticleCategories.create(article = article1, category = category2)
            ArticleCategories.create(article = article1, category = category3)

            ArticleCategories.create(article = article2, category = category1)
            ArticleCategories.create(article = article2, category = category2)
            ArticleCategories.create(article = article2, category = category3)

            ArticleCategories.create(article = article3, category = category1)
            ArticleCategories.create(article = article3, category = category2)
            ArticleCategories.create(article = article3, category = category3)


            ArticleCategories.create(article = article4, category = category1)
            ArticleCategories.create(article = article4, category = category2)

            ArticleCategories.create(article = article5, category = category1)
            ArticleCategories.create(article = article5, category = category2)
            ArticleCategories.create(article = article5, category = category3)

            ArticleCategories.create(article = article6, category = category2)

            ArticleCategories.create(article = article7, category = category4)


            sel = article1.get_similar_articles()

            self.assertIn("test article2", str(tuple(sel)))
            self.assertIn("test article3", str(tuple(sel)))
            self.assertIn("test article5", str(tuple(sel)))
            self.assertNotIn("test article1", str(tuple(sel)))
            self.assertNotIn("test article4", str(tuple(sel)))


            sel = article1.get_similar_articles(limit = 4)


            self.assertIn("test article2", str(tuple(sel)))
            self.assertIn("test article3", str(tuple(sel)))
            self.assertIn("test article5", str(tuple(sel)))
            self.assertIn("test article4", str(tuple(sel)))
            self.assertNotIn("test article6", str(tuple(sel)))
            self.assertNotIn("test article1", str(tuple(sel)))


            sel = article1.get_similar_articles(common_categories = 3, limit = 5)

            self.assertIn("test article2", str(tuple(sel)))
            self.assertIn("test article3", str(tuple(sel)))
            self.assertIn("test article5", str(tuple(sel)))
            self.assertNotIn("test article1", str(tuple(sel)))
            self.assertNotIn("test article4", str(tuple(sel)))



            sel = article7.get_similar_articles()

            self.assertEquals(sel.wrapped_count(False), 0)

            # Test getting article categories while we're at it

            q = article1.get_article_categories()
            
            self.assertIn("test1",str(tuple(q)) )
            self.assertIn("test2",str(tuple(q)))
            self.assertNotIn("test4", str(tuple(q)))
            q = article4.get_article_categories()
            self.assertIn("test1",str(tuple(q)) )
            self.assertNotIn("test3", str(tuple(q)))

            q = article7.get_article_categories()
            self.assertIn("test4",str(tuple(q)) )
            self.assertNotIn("test3", str(tuple(q)))

            query = article1.save_article_categories(["test4", "fundis", "clamo"])

        
    def test_saving_and_deleting_categories(self):

        with test_database(db, (Users, Articles, Categories, ArticleCategories)):
            Users.create_user(username = "konrad", password = "test")
            user1 = Users.select().get()

            art = Articles.create_article(title = "test article1", body = "test", draft = True, author = user1)
            art2 = Articles.create_article(title = "test article2", body = "test", draft = True, author = user1)


            art.save_article_categories(["cat1", "cat2", "cat3"])

            self.assertIn("cat1", str(tuple(art.get_article_categories())))
            self.assertIn("cat2", str(tuple(art.get_article_categories())))
            self.assertIn("cat3", str(tuple(art.get_article_categories())))

            art.save_article_categories(["cat1", "cat2", "cat3"])

            cat = Categories.select().count()

            self.assertEquals(3, cat)

            cat4 = Categories.create(name = "cat4")
            cat5 = Categories.create(name = "cat5")
            cat6 = Categories.create(name = "cat6")

            art.save_article_categories(["cat4"])
            self.assertIn("cat4", str(tuple(art.get_article_categories())))
            self.assertEquals(4, art.get_article_categories().count())

            art2.save_article_categories(("cat1", "cat4", "cat7"))

            cats = Categories.select().group_by(Categories.name)

            self.assertIn("cat7", str(tuple(cats)))
            self.assertEquals(7, cats.count())

            art.delete_instance(recursive = True)

            self.assertEquals(7, cats.count())


            self.assertEquals(ArticleCategories.select().group_by(ArticleCategories.id).count(), 3)
            cat4.delete_instance(recursive = True)

            self.assertEquals(ArticleCategories.select().group_by(ArticleCategories.id).count(), 2)


            

if __name__ == "__main__":
    unittest.main()


