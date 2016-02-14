

from os import path
import sys

class ResGetAttr(object):
    
    def __init__(self, path, dirname):
        self.path = path
        self.dir = dirname
        self.map = {}
    
    def __getitem__(self, f):
        if f not in self.map:
            self[f] = lambda *args, **kwargs: open(self.path.join(self.dir, f), *args, **kwargs)
        return self.map[f]
        
    def __setitem__(self, f, val):
        self.map[f] = val

    def __getattr__(self, name):
        name = self.path.join(self.dir, name)
        if self.path.isdir(name):
            return self.__class__(self.path, name)
        raise AttributeError(name)



sys.modules[__name__] = ResGetAttr(path, path.dirname(__file__))

