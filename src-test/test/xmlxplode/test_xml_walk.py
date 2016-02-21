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



