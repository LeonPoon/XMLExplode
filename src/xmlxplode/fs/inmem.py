'''
Created on 14 Feb 2016

@author: szeleung
'''

from functools import partial
from collections import defaultdict


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
        self.written.append(o)


class Reader(Operator):
    pass

class InMemFs(defaultdict):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        super(InMemFs, self).__init__(partial(self.__class__, parent=self))
        self.parent = parent

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
