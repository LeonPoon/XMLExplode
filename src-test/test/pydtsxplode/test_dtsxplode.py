'''
Created on 14 Feb 2016

@author: szeleung
'''
import unittest

from test import res
from xmlxplode.fs.inmem import InMemFs
from pydtsxplode import DtsxExploder

dtsx_res = res.pydtsxplode.dtsx  # @UndefinedVariable



class TestDtsxplode(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testExplode(self):
        fs = InMemFs()
        source = dtsx_res['Package.dtsx']('rb')
        DtsxExploder.explode(source, fs)
        #self.assertIsInstance(fs['Executable.xml'], basestring)
        fs.writeOut('x')


if __name__ == "__main__":
    unittest.main()
