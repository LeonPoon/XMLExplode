'''
Created on 14 Feb 2016

@author: szeleung
'''
import unittest

from test import res
from xmlxplode.fs.inmem import InMemFs

dtsx_res = res.pydtsxplode.dtsx  # @UndefinedVariable


from xmlxplode.xploder import Exploder as x

class TestExplode(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testExplode(self):
        fs = InMemFs()
        source = dtsx_res['Package.dtsx']('rb')
        x.explode(source, fs)
        self.assertIsInstance(fs['Executable.xml'], basestring)
        open('/home/people/szeleung/Package2.dtsx', 'wb').write(fs['Executable.xml'])


if __name__ == "__main__":
    unittest.main()
