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

class TestFsBase(object):


    def setUp(self):
        self.fs = self.setUpFs()


    def tearDown(self):
        pass


    def test_getRelativePathFrom(self):
        fs = self.fs
        self.assertEqual('.', fs.getRelativePathFrom(fs))
        self.assertEqual('x', fs.getRelativePathFrom(fs, 'x'))
        joint = []
        for x in 'qwerty':
            fs = fs.relativeFs(x)
            joint.append(x)
            self.assertEqual('/'.join(joint), fs.getRelativePathFrom(self.fs))
            self.assertEqual('%s/x' % '/'.join(joint), fs.getRelativePathFrom(self.fs, 'x'))
        self.assertEqual('q/w/e/r/t/y', fs.getRelativePathFrom(self.fs))
        self.assertEqual('q/w/e/r/t/y/x', fs.getRelativePathFrom(self.fs, 'x'))

