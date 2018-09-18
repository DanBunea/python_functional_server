from database_read_services import collect_query_parameters, generate_queries
from database_write_services import Article, Comment, Session
from functional import compose_list
from immutable import Immutable, change
from tests.base_test import BaseTest


class DatabaseQueryTests(BaseTest):

    def test_collect_query_parameters(self):

        json = {
            "find":["id","title", "content",{"comments":["id","comment"]}],
            "where":{"id":13}
        }

        initial_state = Immutable(data=None, errors=[])
        process = compose_list([
            change("json", json),
            change("type", Article),
            collect_query_parameters
        ])

        final_state =  process(initial_state)

        qp = final_state.query_parameters

        self.assertEquals(qp["properties"], [Article.id, Article.title, Article.content, Comment.id, Comment.comment])
        self.assertEquals(qp["joins"], [Article.comments])
        self.assertEquals(str(qp["conditions"][0]), str(Article.id==13))


    def test_generate_queries(self):
        qp={
            "properties": [Article.id, Article.title, Article.content, Comment.id, Comment.comment],
            "joins":[Article.comments],
            "conditions":[Article.id==13]
        }
        session = Session()

        initial_state = Immutable(data=None, errors=[])
        process = compose_list([
            change("query_parameters", qp),
            change("type", Article),
            change("session", session),
            generate_queries
        ])

        final_state =  process(initial_state)

        queries = final_state.queries

        self.assertEquals(str(queries["query_ids"]),str(session.query(Article.id).outerjoin(Article.comments).filter(Article.id==13).group_by(Article.id)))
        self.assertEquals(str(queries["query"]),str(session.query(Article.id, Article.title, Article.content, Comment.id, Comment.comment).outerjoin(Article.comments).group_by(Article.id, Article.title, Article.content, Comment.id, Comment.comment)))


    def test_run_queries(self):
        session = Session()
        queries={
            "query_ids":session.query(Article.id).outerjoin(Article.comments).filter(Article.id==13).group_by(Article.id),
            "query":session.query(Article.id, Article.title, Article.content, Comment.id, Comment.comment).outerjoin(Article.comments).group_by(Article.id, Article.title, Article.content, Comment.id, Comment.comment)
        }

        initial_state = Immutable(data=None, errors=[])
        process = compose_list([
            change("queries", queries),
            change("type", Article),
            change("session", session),
            run_queries
        ])

        final_state =  process(initial_state)

        queries = final_state.queries


