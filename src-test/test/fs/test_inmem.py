'''
Created on 16 Feb 2016

@author: szeleung
'''
import unittest
from test.fs import test_fs_base
from xmlxplode.fs.inmem import InMemFs


class TestInMem(test_fs_base.TestFsBase):

    def setUpFs(self):
        return InMemFs()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    