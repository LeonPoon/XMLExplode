'''
Created on 14 Feb 2016

@author: szeleung
'''
import unittest

from test import res

class TestRes(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_hasattr(self):
        self.assertTrue(hasattr(res, 'pydtsxplode'))

    def test_readRes(self):
        f = res.pydtsxplode.dtsx['Package.dtsx']('rb')  # @UndefinedVariable
        try:
            self.assertTrue(f.read())
        finally:
            f.close()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    

