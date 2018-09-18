import json
import unittest

from api import app


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        print "done"


    def postJson(self, url, myJson, verifyJsonResponse=True):
        sentData =json.dumps(myJson)
        print "POST: "+url+" sent: "+sentData

        rv = self.client.post(url,  data=sentData,
            content_type='application/json' )

        print "RESPONSE: "+rv.data
        if verifyJsonResponse:
            assert rv.mimetype == 'application/json'

        res =  json.loads(rv.data)
        if res.has_key("data"):
            return json.loads(rv.data)["data"]
        else:
            return res


    def compareRecursively(self, a,b,excludeProperties, debug=False):
        if a==None:
            self.assertIsNone(b,"both should be none, but b was "+str(b))
        else:
            if isinstance(a, list):
                where = range(0, len(a))
                self.assertEqual(len(a), len(b),"Lists have different number of elements: "+str(len(a))+"!="+str(len(b))+","+str(a)+":"+str(b))
            else:
                where = a.keys()

            for prop in where:
                # print "Now ",prop,a,b
                ela = a[prop]
                if isinstance(b, dict):
                    self.assertTrue(b.has_key(prop), "key "+prop+" doesn't exist in "+str(b)+" where "+str(a)+" has.")
                if isinstance(b, list):
                    self.assertTrue(len(b)>prop)
                elb = b[prop]
                # if self.debug:
                #     print  "compare: ",prop,ela,elb

                self.compareElement(prop,ela,elb,excludeProperties)

    def compareElement(self, prop, ela, elb, excludeProperties):

        if isinstance(ela, (str, unicode)) or isinstance(ela, (int, long, float)):
            comment = "Comparing for "
            comment = comment + prop + "/"
            comment = str(comment) + str(ela) + "/"
            comment = str(comment) + str(elb)

            if excludeProperties != None:

                if not (prop in excludeProperties):
                    # print "not excluded"+str(prop)
                    self.assertEqual(ela, elb, comment)
                    # self.assertEqual(ela,elb,"Comparing for "+str(prop)+"/"+str(ela)+"/"+str(elb))
                # else:
                #    print "excluded"+str(prop)
            else:
                # print "no excludes"
                self.assertEqual(ela, elb, comment)
                # self.assertEqual(ela,elb,"Comparing for "+str(prop)+"/"+str(ela)+"/"+str(elb))
        else:
            if not (prop in excludeProperties):
                self.compareRecursively(ela, elb, excludeProperties)



