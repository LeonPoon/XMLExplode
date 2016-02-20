'''
Created on 14 Feb 2016

@author: szeleung
'''
from .comp import ComponentBase
from xml.dom import Node, XMLNS_NAMESPACE



import simple_xml_utils as x
import codecs
from xmlxplode import BOM_LOOKUP

SKIP_NS = set([XMLNS_NAMESPACE])




class StringComponentBase(ComponentBase):
    
    def __init__(self, data):
        self.data = data

    def getXIncludeParseType(self):
        return 'text'


class StringComponent(StringComponentBase):

    def writeInto(self, parentElem):
        parentElem.appendChild(parentElem.ownerDocument.createTextNode(self.data))
    
class CDataComponent(StringComponentBase):

    def __init__(self, data, fileName=None, subFolderName='.', encoding=None):
        super(CDataComponent, self).__init__(data)
        self.fileName = fileName
        self.subFolderName = subFolderName
        self.encoding = encoding

    def getFileName(self):
        return self.fileName

    def writeInto(self, container):
        if self.fileName:
            data = self.data
            if self.encoding:
                codec = codecs.lookup(self.encoding)
                bom = BOM_LOOKUP.get(codec)
                if bom:
                    container.write(bom)
                data, _ = codecs.getencoder(self.encoding)(data)
            container.write(data)
        else:
            container.appendChild(container.ownerDocument.createCDATASection(self.data))

    def getComponentSubPath(self):
        return self.subFolderName


class XmlComponent(ComponentBase):

    def __init__(self, fromElem=None):
        '''
        Constructor
        '''
        if fromElem:
            self.fromElem(fromElem)
        else:
            self.clear()

    def clear(self):
        self.components = []
        self.properties = {}
        self.namespaces = {}

    def fromElem(self, elem):
        self.clear()

        self.namespaceURI, self.prefix, self.localName = x.getNameWithNS(elem.namespaceURI, elem.prefix, elem.nodeName)
        self.prefix = self.mapNamespace(self.namespaceURI, prefix=self.prefix)

        for attr in xrange(len(elem.attributes)):
            attr = elem.attributes.item(attr)
            ns, _, n = x.getNameWithNS(attr.namespaceURI, attr.prefix, attr.nodeName)
            if ns not in SKIP_NS:
                self.setProperty(ns, n, attr.value)

        for n in elem.childNodes:
            nodeType = n.nodeType
            (
             self.addComponentFromXml if nodeType == Node.ELEMENT_NODE else
             self.addComponentFromXmlString if nodeType == Node.TEXT_NODE else
             self.addComponentFromXmlCData if nodeType == Node.CDATA_SECTION_NODE else
             self.handleUnknownNode)(n)

    def handleUnknownNode(self, node):
        nodeType = node.nodeType
        raise ValueError('%d=%s' % (nodeType, x.getNodeTypeName(nodeType)))

    def addComponentFromXml(self, xml):
        self.addComponentRaw(self.getComponentClass(xml)(xml))

    def getComponentClass(self, xml):
        return self.__class__

    def addComponentFromXmlString(self, xml):
        self.addComponentRaw(StringComponent(xml.data))

    def addComponentFromXmlCData(self, xml):
        self.addComponentRaw(CDataComponent(xml.data))

    def addComponentRaw(self, component):
        self.components.append(component)

    def setProperty(self, namespaceURI, name, value, prefix=None):
        if namespaceURI:
            prefix = self.mapNamespace(namespaceURI, prefix=prefix)
        self.properties[(namespaceURI, name)] = value

    def mapNamespace(self, namespaceURI, prefix='ns'):
        if not namespaceURI:
            return None
        if namespaceURI not in self.namespaces:
            newPrefix = prefix
            last = 0
            while newPrefix in self.namespaces.values():
                last = last + 1
                newPrefix = '%s_%d' % (prefix, last)
            self.namespaces[namespaceURI] = newPrefix
        return self.namespaces[namespaceURI]

    def getNamespaceURI(self):
        return self.namespaceURI

    def getLocalName(self):
        return self.localName

    def getComponents(self):
        return self.components

    def getProperties(self):
        return self.properties

    def isWriteTextFile(self):
        return False

    def writeInto(self, elem):
        for (ns, name), val in self.getProperties().iteritems():
            prefix = x.makeNamespacePrefix(elem, ns, prefered_prefix=self.mapNamespace(ns))
            elem.setAttributeNS(ns, '%s:%s' % (prefix, name) if prefix else name, val)

    def __str__(self, *args, **kwargs):
        return '%s(%r)' % (ComponentBase.__str__(self, *args, **kwargs), self.getLocalName())
