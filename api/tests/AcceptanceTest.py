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
        self.compareRecursively(article_and_comments, saved_article_with_comments,["id"])



        # expected_articles={
        #     saved_article["id"]:{
        #         "title": "New article",
        #         "content": "The content",
        #         "comments":{
        #             "113":{"comment": "This was awesome!"},
        #             "114":{"comment": "I loved it as well!"}
        #         }
        #     }
        # }
        #
        # articles = self.postJson("/api/1/query/Article", {
        #     "find": ["id","title","content",{"comments":["id","comment"]}],
        #     "where":{"id":saved_article["id"]}})
        #
        #
        # self.compareRecursively(expected_articles, articles,["id"])


