'''
Created on 14 Feb 2016

@author: szeleung
'''
import unittest

from xmlxplode.xmlcomp import XmlComponent

class TestXmlComp(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testNamespace(self):
        c = XmlComponent()
        ns = c.mapNamespace('abc')
        self.assertEqual({'abc': ns}, c.namespaces)
        self.assertEqual(ns, c.mapNamespace('abc', 'cde'))
        c.mapNamespace('abcf', 'cde')
        self.assertEqual({'abc': ns, 'abcf': 'cde'}, c.namespaces)
        c.mapNamespace('abcg', 'cde')
        self.assertEqual({'abc': ns, 'abcf': 'cde', 'abcg': 'cde_1'}, c.namespaces)


if __name__ == "__main__":
    unittest.main()
