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
from libxml2 import XML_ELEMENT_NODE, XML_TEXT_NODE, XML_CDATA_SECTION_NODE, XML_ATTRIBUTE_NODE

import sys


def compareDoms(d1, d2, path):
    compare(d1.documentElement, d2.documentElement, path.sub('/docElem'))


text_node_types = (XML_TEXT_NODE, XML_CDATA_SECTION_NODE)

def findAttr(attr, lst):
    for i in xrange(lst.length):
        a = lst.item(i)
        if (a.localName, a.namespaceURI) == attr:
            return a
    raise LookupError(attr)

def compareAttributes(as1, as2, path):
    l = as1.length
    compare(l, as2.length, path.sub(':length'))
    for i in xrange(l):
        attr = as1.item(i)
        compare(attr, findAttr((attr.localName, attr.namespaceURI), as2), path.sub('[%d]' % i))

def compareNodesGeneric(n1, n2, path):
    nodeType = n1.nodeType
    compare(nodeType, n2.nodeType, path.sub(':nodeType'))
    name = n1.localName
    compare(name, n2.localName, path.sub(':localName'))
    ns = n1.namespaceURI
    compare(ns, n2.namespaceURI, path.sub(':namespaceURI'))
    compareNodes(nodeType, n1, n2, path.sub('=[%s@%s]' % (name, ns)))

def compareNodes(nodeType, n1, n2, path):
    if nodeType == XML_ELEMENT_NODE:
        compareAttributes(n1.attributes, n2.attributes, path.sub(':attributes'))
        compare(n1.childNodes, n2.childNodes, path.sub('/'))
    elif nodeType == XML_ATTRIBUTE_NODE:
        compare(n1.value, n2.value, path.sub(':value'))
    elif nodeType in text_node_types:
        compare(n1.data, n2.data, path.sub(':data'))


def comparePrimitives(v1, v2, path):
    if v1 != v2:
        raise AssertionError('%s: %r vs %r' % (path, v1, v2))
    path.compared(v1, v2)


def compareCollections(c1, c2, path):
    l = len(c1)
    compare(l, len(c2), path.sub(':len'))
    c1 = iter(c1)
    c2 = iter(c2)
    for l in xrange(l):
        compare(next(c1), next(c2), path.sub('[%d]' % l))


prims = (str, bool, unicode, int, type(None))
collecs = (list, tuple)

compares = [
    (lambda x: hasattr(x, 'documentElement'), compareDoms),
    (lambda x: hasattr(x, 'nodeType'), compareNodesGeneric),
    (lambda x: isinstance(x, prims), comparePrimitives),
    (lambda x: isinstance(x, (list, tuple)), compareCollections),
]


class DefaultRoot(object):

    def __init__(self, path):
        self.path = path

    def sub(self, sub):
        return self.__class__('%s%s' % (self.path, sub))

    def compared(self, v1, v2):
        pass

    def __str__(self):
        return self.path


class PrintingRoot(DefaultRoot):

    def compared(self, v1, v2):
        print '%s: %r vs %r' % (self, v1, v2)


def compare(node1, node2, path=DefaultRoot('root')):
    if type(node1) != type(node2):
        raise ValueError('%s: %r vs %r' % (path, type(node1), type(node2)))
    for ts, comp in compares:
        if ts(node1):
            try:
                return comp(node1, node2, path)
            except (AssertionError, TypeError):
                raise
            except:
                _, ex, traceback = sys.exc_info()
                raise AssertionError, '%s:%s' % (path, ex), traceback
    raise TypeError('%s: %s' % (path, str(type(node1))))
