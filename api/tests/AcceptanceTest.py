import json
from tests.base_test import BaseTest


class AcceptanceTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        pass






    def test_save_and_read(self):
        #GIVEN
        article = {
            "title":"New article",
            "content":"The content"
            }
        saved_article = self.postJson("/api/1/save/Article",article)
        self.compareRecursively(article, saved_article,["id"])


        article_and_comments = {"id":saved_article["id"],
                                "comments":[{"comment":"This was awesome!"},{"comment":"I loved it as well!"}]}

        saved_article_with_comments = self.postJson("/api/1/save/Article", article_and_comments)
        self.compareRecursively({"id":saved_article["id"],
                                "title": "New article",
                                "content": "The content"}, saved_article_with_comments,["id"])



        expected_articles={
            str(saved_article["id"]):{
                "title": "New article",
                "content": "The content",
            }
        }

        expected_comment_1 = {"comment": "This was awesome!"}
        expected_comment_2 = {"comment": "I loved it as well!"}

        articles = self.postJson("/api/1/query/Article", {
            "find": ["id","title","content",{"comments":["id","comment"]}],
            "where":{"id":saved_article["id"]}})



        self.compareRecursively( expected_articles, articles,["id"])
        kk1 = articles[str(saved_article["id"])]["comments"].keys()[0]
        kk2 = articles[str(saved_article["id"])]["comments"].keys()[1]
        k1 = str(kk1) if kk1<kk2 else str(kk2)
        k2 = str(kk2) if kk2>kk1 else str(kk1)
        self.compareRecursively( expected_comment_1,articles[str(saved_article["id"])]["comments"][k1] ,["id"])
        self.compareRecursively( expected_comment_2,articles[str(saved_article["id"])]["comments"][k2] ,["id"])


