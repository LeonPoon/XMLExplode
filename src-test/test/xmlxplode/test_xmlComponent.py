# Copyright (C) 2016 Leon Poon
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
