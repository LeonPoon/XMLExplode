'''
Created on 16 Feb 2016

@author: szeleung
'''
import unittest


class TestFsBase(unittest.TestCase):


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

