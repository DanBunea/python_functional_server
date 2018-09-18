from immutable import Immutable, change, value
from tests.base_test import BaseTest


class ChangeTests(BaseTest):


    def test_change(self):
        #given an immutable object
        initial_state = Immutable(data=None, errors=[])


        #when we channge it
        json = {"name":"Laci"}
        final_state = change("json", json)(initial_state)

        #assert it has the new value
        self.assertEquals(json , value("json")(final_state))
