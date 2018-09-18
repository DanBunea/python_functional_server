from json import loads, dumps

from mock import mock

from database_services import Article, Comment
from functional import compose_list
from immutable import Immutable, change, value
from tests.base_test import BaseTest
from transform_services import transform_from_json, transform_to_json
from api import to_json


def to_json_with_dumps(state):
    return dumps(dict(data=state.data))

class TransformServicesTests(BaseTest):
    def get_transform_from_json(self, json):
        initial_state = Immutable(data=None, errors=[])
        process = compose_list([
            change("json", json),
            change("data", Article()),
            change("type",Article),
            transform_from_json
        ])


        return process(initial_state)

    def test_transform_from_json_article(self):
        # when invoking the function
        json = {"title":"A title", "content":"Some content"}
        final_state = self.get_transform_from_json(json)

        #assert the object contains the values
        transformed_object = value("data")(final_state)


        self.assertEquals(json["title"],transformed_object.title)
        self.assertEquals(json["content"],transformed_object.content)


    def test_transform_from_json_article_with_comments(self):
        # when invoking the function
        json = {
            "title":"A title",
            "content":"Some content",
            "comments":
            [{"comment":"This was awesome!"},{"comment":"I loved it as well!"}]
        }
        final_state = self.get_transform_from_json(json)

        #assert the object contains the values
        transformed_object = value("data")(final_state)


        self.assertEquals(json["title"],transformed_object.title)
        self.assertEquals(json["content"],transformed_object.content)
        self.assertEquals(json["comments"][0]["comment"],transformed_object.comments[0].comment)
        self.assertEquals(json["comments"][1]["comment"],transformed_object.comments[1].comment)



    def test_transform_to_json_article(self):
        initial_state = Immutable(data=None, errors=[])
        process = compose_list([
            change("data", Article(title="title", content="content")),
            change("type",Article),
            transform_to_json
        ])
        final_state =process(initial_state)

        #assert the object contains the values
        json = value("data")(final_state)


        self.assertTrue(json.has_key("id"))
        self.assertEquals("title",json["title"])
        self.assertEquals("content",json["content"])

    def test_transform_to_json_article_with_comments(self):
        initial_state = Immutable(data=None, errors=[])
        process = compose_list([
            change("data", Article(title="title", content="content", comments=[Comment(comment="First comment"), Comment(comment="Second comment")])),
            change("type",Article),
            transform_to_json
        ])
        final_state =process(initial_state)

        #assert the object contains the values
        json = value("data")(final_state)

        self.assertTrue(json.has_key("id"))
        self.assertEquals("title",json["title"])
        self.assertEquals("content",json["content"])
        self.assertEquals("First comment",json["comments"][0]["comment"])
        self.assertEquals("Second comment",json["comments"][1]["comment"])



    @mock.patch('api.to_json',side_effect=to_json_with_dumps)
    def test_to_json(self, to_json):
        json = {"title": "A title", "content": "Some content"}
        initial_state = Immutable(data=None, errors=[])
        process = compose_list([
            change("data", json),
            to_json
        ])
        final_state =process(initial_state)

        json_final = loads(final_state)

        #assert the object contains the values
        self.compareRecursively({"data":json}, json_final,[])




