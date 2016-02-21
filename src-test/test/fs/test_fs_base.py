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

