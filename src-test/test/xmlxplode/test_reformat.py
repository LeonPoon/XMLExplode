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

from xmlxplode import reformat







class TestReformat(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def _find(self, s, *a, **kwargs):
        return reformat._find(s, len(s), *a, **kwargs)

    def testFindSimple(self):
        res = self._find("   aa bbb aaa ", 0, 0, reformat._prepare_lookups('aaa', 'bbb'))
        self.assertEqual((9, 9, 'bbb'), res)

    def testFindLongest(self):
        res = self._find("   aabc ", 2, 2, reformat._prepare_lookups('aa', 'aab', 'aabc'))
        self.assertEqual((7, 7, 'aabc'), res)

    def testFindLongestAfter(self):
        res = self._find("  \n aaabc ", 1, 1, reformat._prepare_lookups('aa', 'aab', 'aabc'))
        self.assertEqual((6, 3, 'aa'), res)

    def testFindEof(self):
        s = "  \n a"
        res = self._find(s, 1, 1, reformat._prepare_lookups('aa', 'aab', 'aabc'))
        self.assertEqual(reformat.Found(len(s), 2, False), res)

    def testFindCommonSuffix(self):
        res = self._find('x/>  <', 1, 1, reformat._prepare_lookups('>', '/>'))
        self.assertEqual((3, 3, '/>'), res)

    def testLines(self):
        l = len(reformat._lines) + 10
        self.assertEqual(' ' * l, reformat._lines[l])
        self.assertEqual(l + 1, len(reformat._lines))

    def testFormat1(self):
        f = reformat.reformat('''
<?xml something ?>
<x a='b' c="d'">
   <y>
     <z/>
       <a b="c"/>
 </y>
</x>
''', sep='\n')
        exp = '''
<?xml something ?>
<x
 a='b'
 c="d'"
 >
   <y>
     <z/>
       <a
        b="c"
        />
 </y>
</x>
'''
        self.assertEqual(exp, f)

if __name__ == "__main__":
    unittest.main()
