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
