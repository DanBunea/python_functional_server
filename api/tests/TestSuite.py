import unittest


from tests.AcceptanceTest import AcceptanceTest
from tests.ApiTests import ApiTests
from tests.ChangeTests import ChangeTests
from tests.DatabaseQueryTests import DatabaseQueryTests
from tests.DatabaseServicesTests import DatabaseServicesTests
from tests.TransformServicesTests import TransformServicesTests


def suite():


    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(AcceptanceTest))
    suite.addTest(unittest.makeSuite(ApiTests))
    suite.addTest(unittest.makeSuite(ChangeTests))
    suite.addTest(unittest.makeSuite(DatabaseServicesTests))
    suite.addTest(unittest.makeSuite(TransformServicesTests))
    suite.addTest(unittest.makeSuite(DatabaseQueryTests))

    return suite


if __name__ == '__main__':
    all = suite()
    unittest.TextTestRunner(verbosity=0).run(all)
