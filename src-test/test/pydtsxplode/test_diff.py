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
import StringIO
import os
import unittest
from functools import partial

from dtsxdiff import findDiffs, printDiff
from test import res
from xmlxplode.fs.inmem import InMemFs

dtsx_res = res.pydtsxplode.dtsx  # @UndefinedVariable



class TestDtsxDiff(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testMakeDiffs(self):
        fs1 = InMemFs()
        fs2 = InMemFs()

        fs1['dir']['file1'] = 'ab\r\nbc\r\ncd'
        fs2['dir']['file1'] = 'ab\r\nBc\r\ncd'

        fs1['X']['file2'] = 'X is dir\n'
        fs2['X'] = 'X is file\n'.replace('\n', os.linesep)

        fs1['dir2']['file3'] = ''
        fs2['dir3']['file3'] = ''

        diffs = findDiffs(['left'], fs1, ['right'], fs2)
        out = StringIO.StringIO()
        map(partial(printDiff, out=out, sep='|'), diffs)
        out = out.getvalue().replace('\r\n', '\n').split('\n')
        self.assertEqual(11, len(out))
        self.assertEqual('', out[-1])
        self.assertIn('File left|X is a directory while file right|X is a regular file', out)
        idx = out.index('--- left|dir|file1')
        for line in [
                    '+++ right|dir|file1',
                    '@@ -1,3 +1,3 @@',
                    ' ab',
                    '-bc',
                    '+Bc',
                    ' cd',
                    'Only in left: dir2',
                    'Only in right: dir3',
                ]:
            idx += 1
            self.assertEquals(line, out[idx])
        self.assertIn('Only in left: dir2', out)
        self.assertIn('Only in right: dir3', out)


if __name__ == "__main__":
    unittest.main()
