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

