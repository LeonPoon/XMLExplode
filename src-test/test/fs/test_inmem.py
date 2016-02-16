'''
Created on 16 Feb 2016

@author: szeleung
'''
import unittest
from xmlxplode.fs.inmem import InMemFs
from test.fs.test_fs_base import TestFsBase


class TestInMem(TestFsBase, unittest.TestCase):

    def setUpFs(self):
        return InMemFs()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    