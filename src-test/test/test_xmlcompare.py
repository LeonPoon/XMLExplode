# Copyright 2016 Leon Poon and Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



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


