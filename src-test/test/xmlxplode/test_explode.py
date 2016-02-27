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
from test import xmlcompare
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
        source = dtsx_res['Package.dtsx']('rb').read()
        x.explode(source, fs)
        xmlstr = fs['Executable.xml']
        self.assertIsInstance(xmlstr, basestring)
        xmlcompare.compare(minidom.parseString(xmlstr), minidom.parseString(source), xmlcompare.DefaultRoot(self.id()))


if __name__ == "__main__":
    unittest.main()
