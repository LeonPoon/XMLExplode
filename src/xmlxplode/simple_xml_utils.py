'''
Created on 14 Feb 2016

@author: szeleung
'''


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


