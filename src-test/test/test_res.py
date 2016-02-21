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

from test import res

class TestRes(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_hasattr(self):
        self.assertTrue(hasattr(res, 'pydtsxplode'))

    def test_readRes(self):
        f = res.pydtsxplode.dtsx['Package.dtsx']('rb')  # @UndefinedVariable
        try:
            self.assertTrue(f.read())
        finally:
            f.close()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    

