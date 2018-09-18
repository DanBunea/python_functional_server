from random import random

from database_services import Session, get_database_object, Article, save_database_object
from functional import compose_list
from immutable import Immutable, value, change
from tests.base_test import BaseTest


class DatabaseServicesTests(BaseTest):


    def get_database_object_for(self, json, session):
        initial_state = Immutable(data=None, errors=[])
        process = compose_list([
            change("json", json),
            change("session", session),
            change("type", Article),
            get_database_object
        ])


        return process(initial_state)

    def test_get_new_database_object(self):
        # when invoking the function with no id in the json
        final_state = self.get_database_object_for({}, Session())

        #assert it returns a new object, associated with the session
        new_object = value("data")(final_state)
        self.assertEquals(Article, type(new_object))


    def test_get_existing_database_object(self):
        #given an exising object in the database
        session = Session()
        new_article = Article(title="Title", content="Content")
        session.add(new_article)
        session.commit()
        id = new_article.id
        session.close()

        # when invoking the function with no id in the json
        final_state = self.get_database_object_for({"id":id}, Session())

        #assert it returns a new object, associated with the session
        existing_object = value("data")(final_state)
        self.assertEquals(Article, type(existing_object))
        self.assertEquals("Title", existing_object.title)


    def test_save_database_object(self):
        initial_state = Immutable(data=None, errors=[])
        title = "Saved "+str(random())
        process = compose_list([
            change("data", Article(title=title, content="Added content")),
            change("session", Session()),
            save_database_object
        ])

        final_state =  process(initial_state)

        # assert it exists in the database
        saved_object = Session().query(Article).filter(Article.title==title).first()
        self.assertEquals(title, saved_object.title)
        self.assertEquals("Added content", saved_object.content)



