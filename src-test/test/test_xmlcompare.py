# Copyright (C) 2016 Leon Poon and Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>



import unittest
from xml.dom import minidom

from test.xmlcompare import DefaultRoot, compare

class TestXmlCompare(unittest.TestCase):


    def setUp(self):
        self.root = DefaultRoot(self.id())


    def tearDown(self):
        pass

    def test_compare(self):
        compare(1, 1, self.root)

    def test_compare_diff(self):
        with self.assertRaises(AssertionError):
            compare(1, 2, self.root)

    def test_compare_dom(self):
        d1 = minidom.getDOMImplementation().createDocument('x', 'y:n1', None)
        d1.documentElement.setAttributeNS('y', 'a:A', 'val1')
        d1.documentElement.appendChild(d1.createTextNode('abc'))
        d2 = minidom.getDOMImplementation().createDocument('x', 'z:n1', None)
        d2.documentElement.setAttributeNS('y', 'b:A', 'val1')
        d2.documentElement.appendChild(d2.createTextNode('abc'))
        compare(d1, d2, self.root)

    def test_compare_dom_diff_name(self):
        with self.assertRaises(AssertionError):
            d1 = minidom.getDOMImplementation().createDocument('x', 'y:n1', None)
            d2 = minidom.getDOMImplementation().createDocument('x', 'z:n2', None)
            compare(d1, d2, self.root)

    def test_compare_dom_diff_ns(self):
        with self.assertRaises(AssertionError):
            d1 = minidom.getDOMImplementation().createDocument('x', 'z:n1', None)
            d2 = minidom.getDOMImplementation().createDocument('y', 'z:n1', None)
            compare(d1, d2, self.root)

    def test_compare_dom_diff_attr(self):
        with self.assertRaises(AssertionError): # diff val
            d1 = minidom.getDOMImplementation().createDocument('x', 'y:n1', None)
            d1.documentElement.setAttributeNS('y', 'a:A', 'val1')
            d2 = minidom.getDOMImplementation().createDocument('x', 'y:n1', None)
            d1.documentElement.setAttributeNS('y', 'a:A', 'val2')
            compare(d1, d2, self.root)
        with self.assertRaises(AssertionError): # diff ns
            d1 = minidom.getDOMImplementation().createDocument('x', 'y:n1', None)
            d1.documentElement.setAttributeNS('y', 'a:A', 'val1')
            d2 = minidom.getDOMImplementation().createDocument('x', 'y:n1', None)
            d1.documentElement.setAttributeNS('z', 'a:A', 'val1')
            compare(d1, d2, self.root)
        with self.assertRaises(AssertionError): # diff name
            d1 = minidom.getDOMImplementation().createDocument('x', 'y:n1', None)
            d1.documentElement.setAttributeNS('y', 'a:A', 'val1')
            d2 = minidom.getDOMImplementation().createDocument('x', 'y:n1', None)
            d1.documentElement.setAttributeNS('y', 'a:B', 'val1')
            compare(d1, d2, self.root)

    def test_compare_dom_diff_children(self):
        with self.assertRaises(AssertionError):  # diff name
            d1 = minidom.getDOMImplementation().createDocument('x', 'y:n1', None)
            d1.documentElement.appendChild(d1.createElementNS('c', 'A:B'))
            d2 = minidom.getDOMImplementation().createDocument('x', 'z:n1', None)
            d2.documentElement.appendChild(d1.createElementNS('c', 'A:C'))
            compare(d1, d2, self.root)
        with self.assertRaises(AssertionError):  # diff ns
            d1 = minidom.getDOMImplementation().createDocument('x', 'y:n1', None)
            d1.documentElement.appendChild(d1.createElementNS('c', 'A:B'))
            d2 = minidom.getDOMImplementation().createDocument('x', 'z:n1', None)
            d2.documentElement.appendChild(d1.createElementNS('d', 'A:B'))
            compare(d1, d2, self.root)
        with self.assertRaises(AssertionError):  # diff length
            d1 = minidom.getDOMImplementation().createDocument('x', 'y:n1', None)
            d1.documentElement.appendChild(d1.createElementNS('c', 'A:B'))
            d2 = minidom.getDOMImplementation().createDocument('x', 'z:n1', None)
            compare(d1, d2, self.root)


if __name__ == "__main__":
    unittest.main()


