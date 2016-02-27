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

from xml.dom import XMLNS_NAMESPACE, Node

def getNameWithNS(namespace_uri, prefix, node_name):
    localName = node_name[len(prefix) + 1:] if prefix else node_name
    return namespace_uri, prefix, localName


def makeNamespacePrefix(elem, namespaceURI, prefered_prefix='ns'):
    if not namespaceURI:
        return None
    elem = elem.ownerDocument.documentElement
    used = []
    for attr in xrange(len(elem.attributes)):
        attr = elem.attributes.item(attr)
        if attr.namespaceURI == XMLNS_NAMESPACE:
            _, _, prefix = getNameWithNS(XMLNS_NAMESPACE, attr.prefix, attr.nodeName)
            used.append(prefix)
            if attr.value == namespaceURI:
                return prefix
    used = set(used)
    prefix = prefered_prefix
    last = 0
    while prefix in used:
        last = last + 1
        prefix = '%s_%d' % (prefered_prefix, last)
    elem.setAttributeNS(XMLNS_NAMESPACE, 'xmlns:%s' % prefix, namespaceURI)
    return prefix
    


def getNodeTypeName(nodeType):
    for attr in dir(Node):
        if attr.endswith('_NODE') and getattr(Node, attr) == nodeType:
            return attr
    return None


