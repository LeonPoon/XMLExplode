'''
Created on 14 Feb 2016

@author: szeleung
'''

from xml.dom import minidom

import simple_xml_utils as x
from xmlcomp import StringComponent, CDataComponent, XmlComponent 

XInclude_NS = 'http://www.w3.org/2001/XInclude'



class BasicXmlComponent(XmlComponent):
    
    def getFileName(self):
        return '%s.xml' % self.getLocalName()


class Exploder(object):
    '''
    classdocs
    '''

    def __init__(self, source, fs):
        self.fs = fs
        if hasattr(source, 'open'):
            source = source.open('rb')
        self.dom = minidom.parse(source)
        self.domImpl = minidom.getDOMImplementation()

    @classmethod
    def explode(cls, source, fs):
        return cls(source, fs)._explode()

    def _explode(self):
        root = self.rootElement(self.dom.documentElement)
        self.writeComponent(self.fs, root, None)

    def rootElement(self, elem):
        return BasicXmlComponent(elem)

    def writeComponent(self, fs, comp, parentElem):
        fileName = None
        if isinstance(comp, StringComponent):
            parentElem.appendChild(parentElem.ownerDocument.createTextNode(comp))
        elif isinstance(comp, CDataComponent):
            parentElem.appendChild(parentElem.ownerDocument.createCDATASection(comp))
        elif comp.getFileName():
            fs, fileName = self.writeComponentFile(fs, comp)
        else:
            self.writeComponentIntoParent(fs, comp, parentElem)
        return fs, fileName

    def writeComponentFile(self, fs, comp):
        fileName = comp.getFileName()

        namespaceURI = comp.getNamespaceURI()
        name = '%s:%s' % (comp.mapNamespace(namespaceURI), comp.getLocalName()) if namespaceURI else comp.getLocalName()
        dom = self.domImpl.createDocument(namespaceURI, name, None)
        elem = dom.documentElement
        x.makeNamespacePrefix(elem, namespaceURI, prefered_prefix=comp.mapNamespace(namespaceURI))

        subFs = fs.relativeFs(comp.getSubFolderName())

        self.writeComponentElement(comp, elem)
        self.writeComponents(subFs, comp, elem)

        with subFs.open(fileName, 'wb') as f:
            dom.writexml(f, encoding=self.dom.encoding)
        return subFs, fileName

    def writeComponentIntoParent(self, fs, comp, parentElem):
        dom = parentElem.ownerDocument
        namespaceURI = comp.getNamespaceURI()
        prefix = x.makeNamespacePrefix(parentElem, namespaceURI, prefered_prefix=comp.mapNamespace(namespaceURI))
        elem = dom.createElementNS(comp.getNamespaceURI(), '%s:%s' % (prefix, comp.getLocalName()) if prefix else comp.getLocalName())
        parentElem.appendChild(elem)
        self.writeComponentElement(comp, elem)
        self.writeComponents(fs, comp, elem)
        return None, None

    def writeComponentElement(self, comp, elem):
        for (ns, name), val in comp.getProperties().iteritems():
            prefix = x.makeNamespacePrefix(elem, ns, prefered_prefix=comp.mapNamespace(ns))
            elem.setAttributeNS(ns, '%s:%s' % (prefix, name) if prefix else name, val)

    def writeComponents(self, fs, comp, parentElem):
        for subComp in comp.getComponents():
            subFs, subName = self.writeComponent(fs, subComp, parentElem)
            if subName:
                subName = subFs.getRelativePathFrom(fs, subName)
                elem = parentElem.ownerDocument.createElementNS(XInclude_NS, 'xi:include')
                elem.setAttributeNS(XInclude_NS, 'xi:href', subName)
                parentElem.appendChild(elem)
