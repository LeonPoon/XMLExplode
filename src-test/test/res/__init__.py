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

