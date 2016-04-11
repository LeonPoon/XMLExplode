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

from dtsxdiff import findDiffs, printDiff, splitForDiff
from test import res
from xmlxplode.fs.inmem import InMemFs

dtsx_res = res.pydtsxplode.dtsx  # @UndefinedVariable



class TestDtsxDiff(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_split_for_diff_no_eol(self):
        self.assertEquals([
            'ab\n',
            'c',
        ], splitForDiff('ab\nc'))

    def test_split_for_diff_1_eol(self):
        self.assertEquals([
            'ab\n',
            'c\n',
        ], splitForDiff('ab\nc\n'))

    def test_split_for_diff_many_eol(self):
        self.assertEquals([
            'ab\n',
            'c\n',
            '\n',
            '\n',
        ], splitForDiff('ab\nc\n\n\n'))

    def test_split_for_diff_mixed_eol(self):
        self.assertEquals([
            'ab\r\n',
            'c\n',
            '\r\n',
            '\n',
        ], splitForDiff('ab\r\nc\n\r\n\n'))

    def testMakeDiffs(self):
        fs1 = InMemFs()
        fs2 = InMemFs()

        fs1['dir']['file1'] = 'ab\r\nbc\r\ncd'
        fs2['dir']['file1'] = 'ab\r\nBc\r\ncd\n'

        fs1['X']['file2'] = 'X is dir\n'
        fs2['X'] = 'X is file\n'.replace('\n', os.linesep)

        fs1['dir2']['file3'] = 'abc\nxyz\n'
        fs1['dir2']['file4'] = ''  # empty

        fs2['dir3']['file3'] = 'def\n'
        fs2['dir3']['file4'] = ''  # empty

        diffs = findDiffs(['left'], fs1, ['right'], fs2)
        out = StringIO.StringIO()
        map(partial(printDiff, out=out, sep='|'), diffs)
        out = out.getvalue().strip().replace('\r\n', '\n').split('\n')
        #for o in out:
        #    print '%r,' % o
        self.assertEqual(len(out), len(set(out)))  # make sure all unique
        asserted = 0
        for line in [
            'File left|X is a directory while file right|X is a regular file',
            'Only in left|dir2: file4',
            'Only in right|dir3: file4',
        ]:
            self.assertIn(line, out)
            asserted += 1
        asserted += self.assertLines([
            '--- left|dir|file1',
            '+++ right|dir|file1',
            '@@ -1,3 +1,3 @@',
            ' ab',
            '-bc',
            '-cd',
            '\\ No newline at end of file',
            '+Bc',
            '+cd',
        ], out)
        asserted += self.assertLines([
            '--- left|dir2|file3',
            '+++ /dev/null',
            '@@ -1,2 +0,0 @@',
            '-abc',
            '-xyz',
        ], out)
        asserted += self.assertLines([
            '--- /dev/null',
            '+++ right|dir3|file3',
            '@@ -0,0 +1 @@',
            '+def',
        ], out)
        self.assertEqual(len(out), asserted)

    def assertLines(self, lines, out):
        idx = out.index(lines[0])
        for line in lines[1:]:
            idx += 1
            self.assertEqual(line, out[idx])
        return len(lines)


if __name__ == "__main__":
    unittest.main()
