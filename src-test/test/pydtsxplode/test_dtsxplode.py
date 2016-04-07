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

from test import res
from xmlxplode.fs.inmem import InMemFs
from pydtsxplode import DtsxExploder
import os

dtsx_res = res.pydtsxplode.dtsx  # @UndefinedVariable



class TestDtsxplode(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testExplode(self):
        fs = InMemFs()
        source = dtsx_res['Package.dtsx']('rb')
        DtsxExploder.explode(source, fs)
        self.assertIsInstance(fs['Package.xml'], basestring)
        # next(fs.writeOut(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.test_output')), None)


if __name__ == "__main__":
    unittest.main()
