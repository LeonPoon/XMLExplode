'''
Created on 14 Feb 2016

@author: szeleung
'''
import unittest
from xml.dom import minidom

from test import res

dtsx_res = res.pydtsxplode.dtsx  # @UndefinedVariable

class TestXml(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testMakeXmlNs(self):
        pass

    def testReadPackage(self):
        f = dtsx_res['Package.dtsx']('rb')
        dom = minidom.parse(f)
        self.assertIs(dom.documentElement.ownerDocument, dom)
        self.assertIs(dom.documentElement.parentNode, dom)


if __name__ == "__main__":
    unittest.main()



