

from mock import mock
from tests.base_test import BaseTest
from api import save



class ApiTests(BaseTest):

    @mock.patch('api.get_database_object')
    @mock.patch('api.change')
    @mock.patch('api.transform_from_json')
    @mock.patch('api.save_database_object')
    @mock.patch('api.transform_to_json')
    @mock.patch('api.to_json')
    def test_save_an_article(self, get_database_object, change, transform_from_json, save_database_object, transform_to_json, to_json):
    # def test_save_an_article(self, change):
        #when
        save({}, None)

        #verify get_database_object_invoked
        change.assert_called()
        get_database_object.assert_called()
        transform_from_json.assert_called()
        save_database_object.assert_called()
        transform_to_json.assert_called()
        to_json.assert_called()