'''
Created on 14 Feb 2016

@author: szeleung
'''

from xml.dom import minidom

import simple_xml_utils as x
from xmlcomp import XmlComponent 

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
        fileName = parse = None
        if comp.getFileName():
            fs, fileName, parse = self.writeComponentFile(fs, comp)
        else:
            self.writeComponentIntoParent(fs, comp, parentElem)
        return fs, fileName, parse

    def writeComponentFile(self, fs, comp):
        fileName = comp.getFileName()
        subFs = fs.relativeFs(comp.getSubFolderName())
        parse = None
        with subFs.open(fileName, 'wb') as f:
            if comp.isWriteTextFile():
                parse = 'text'
                comp.writeInto(f)
            else:
                self.writeComponentXmlFile(subFs, comp, f)
        return subFs, fileName, parse
    
    def writeComponentXmlFile(self, subFs, comp, f):
        namespaceURI = comp.getNamespaceURI()
        name = '%s:%s' % (comp.mapNamespace(namespaceURI), comp.getLocalName()) if namespaceURI else comp.getLocalName()
        dom = self.domImpl.createDocument(namespaceURI, name, None)
        elem = dom.documentElement
        x.makeNamespacePrefix(elem, namespaceURI, prefered_prefix=comp.mapNamespace(namespaceURI))
        comp.writeInto(elem)
        self.writeComponents(subFs, comp, elem)
        dom.writexml(f, encoding=self.dom.encoding)

    def writeComponentIntoParent(self, fs, comp, parentElem):
        if comp.getLocalName():
            elem = self.writeComponentElement(comp, parentElem)
        else:
            elem = parentElem
            comp.writeInto(elem)
        self.writeComponents(fs, comp, elem)

    def writeComponentElement(self, comp, elem):
        dom = elem.ownerDocument
        namespaceURI = comp.getNamespaceURI()
        prefix = x.makeNamespacePrefix(elem, namespaceURI, prefered_prefix=comp.mapNamespace(namespaceURI))
        subElem = dom.createElementNS(comp.getNamespaceURI(), '%s:%s' % (prefix, comp.getLocalName()) if prefix else comp.getLocalName())
        elem.appendChild(subElem)
        comp.writeInto(subElem)
        return subElem

    def writeComponents(self, fs, comp, parentElem):
        for subComp in comp.getComponents():
            subFs, subName, parse = self.writeComponent(fs, subComp, parentElem)
            if subName:
                subName = subFs.getRelativePathFrom(fs, subName)
                elem = parentElem.ownerDocument.createElementNS(XInclude_NS, 'xi:include')
                elem.setAttributeNS(XInclude_NS, 'xi:href', subName)
                if parse:
                    elem.setAttributeNS(XInclude_NS, 'xi:parse', parse)
                parentElem.appendChild(elem)
