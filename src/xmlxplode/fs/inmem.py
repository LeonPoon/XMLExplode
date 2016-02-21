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

import os



class Operator(object):

    def __init__(self, fs, fname):
        self.fs = fs
        self.fname = fname
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Writer(Operator):

    def __init__(self, *args, **kwargs):
        super(Writer, self).__init__(*args, **kwargs)
        self.written = []

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fs[self.fname] = ''.join(self.written)

    def write(self, o):
        self.written.append(str(o))


class Reader(Operator):
    pass

class InMemFs(dict):
    '''
    classdocs
    '''

    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent

    def __missing__(self, key):
        d = self.__class__(name=key, parent=self)
        self[key] = d
        return d

    def relativeFs(self, rel):
        while True:
            oldRel = rel
            rel = oldRel.replace('//', '/')
            if rel == oldRel:
                break
        rels = rel.split('/', 1)
        rel = rels[0]
        if not rel:
            raise ValueError(oldRel)
        elif rel == '.':
            rel = self
        else:
            rel = self[rel]
        return rel if len(rels) == 1 else rel.relativeFs(rels[1])

    def open(self, fname, mode=''):
        return (Writer if 'w' in mode else Reader)(self, fname)

    def getRelativePathFrom(self, fs, subName=None):
        if fs == self:
            return subName if subName else '.'
        fs = self.parent.getRelativePathFrom(fs)
        fs = self.name if fs == '.' else '%s/%s' % (fs, self.name) 
        return '%s/%s' % (fs, subName) if subName else fs 

    def getRoot(self):
        parent = self.parent
        return parent.getRoot() if parent else self

    def writeOut(self, dirpath, yieldFilenames=False):
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
            if yieldFilenames:
                yield '%s%s' % (dirpath, os.path.sep)
        for n, v in self.iteritems():
            p = os.path.join(dirpath, n)
            if isinstance(v, basestring):
                f = open(p, 'wb')
                try:
                    f.write(v)
                finally:
                    f.close()
                if yieldFilenames:
                    yield p
            elif v:
                for p in v.writeOut(p):
                    if yieldFilenames:
                        yield p
                
    def __str__(self):
        root = self.getRoot()
        return '/' if root == self else self.getRelativePathFrom(root)
