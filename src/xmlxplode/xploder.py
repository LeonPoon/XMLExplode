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

from xml.dom import minidom

import simple_xml_utils as x
from xmlcomp import XmlComponent 
import urllib
import codecs
from xmlxplode import BOM_MAP, BOM_LOOKUP
from functools import partial

XInclude_NS = 'http://www.w3.org/2001/XInclude'



class EncodingWriter(object):
    def __init__(self, wrapped, encoding):
        self.write = lambda o: wrapped.write(o.encode(encoding))



class BasicXmlComponent(XmlComponent):
    
    def getFileName(self):
        return '%s.xml' % self.getLocalName()

    def getComponentClass(self, xml):
        return XmlComponent


class Exploder(object):
    '''
    classdocs
    '''
    

    def __init__(self, source, fs):
        self.fs = fs
        if hasattr(source, 'open'):
            f = source.open('rb')
            try:
                source = f.read()
            finally:
                f.close()
        elif hasattr(source, 'read'):
            source = source.read()
        self.eol = "\r\n" if "\r\n" in source else "\n" if "\n" in source else ''
        self.dom = minidom.parseString(source)
        for bom, codec in BOM_MAP.iteritems():
            if source.startswith(bom):
                self.dom.encoding = codec.name
                break
        self.domImpl = minidom.getDOMImplementation()

    @classmethod
    def explode(cls, source, fs):
        return cls(source, fs)._explode()

    def _explode(self):
        root = self.rootElement(self.dom.documentElement)
        self.writeComponent(self.fs, self.fs, root, None)

    def rootElement(self, elem):
        return BasicXmlComponent(elem)

    def writeComponent(self, parentFs, fs, comp, parentElem):
        fileName = parse = None
        if comp.getFileName():
            fs, fileName, parse = self.writeComponentFile(fs, comp)
        else:
            self.writeComponentIntoParent(parentFs, fs, comp, parentElem)
        return fs, fileName, parse

    def writeComponentFile(self, fs, comp):
        fileName = comp.getFileName()
        subFs = fs.relativeFs(comp.getComponentSubPath())
        parse = comp.getXIncludeParseType()
        with subFs.open(fileName, 'wb') as f:
            if parse == 'xml':
                self.writeComponentXmlFile(subFs, comp, f)
            else:
                comp.writeInto(f)
        return subFs, fileName, parse
    
    def writeComponentXmlFile(self, subFs, comp, f):
        namespaceURI = comp.getNamespaceURI()
        name = '%s:%s' % (comp.mapNamespace(namespaceURI), comp.getLocalName()) if namespaceURI else comp.getLocalName()
        dom = self.domImpl.createDocument(namespaceURI, name, None)
        elem = dom.documentElement
        x.makeNamespacePrefix(elem, namespaceURI, prefered_prefix=comp.mapNamespace(namespaceURI))
        comp.writeInto(elem)
        self.writeComponents(subFs, subFs, comp, elem)
        if self.dom.encoding:
            f.write(BOM_LOOKUP[codecs.lookup(self.dom.encoding)])
        dom.writexml(EncodingWriter(f, self.dom.encoding) if self.dom.encoding else f, encoding=self.dom.encoding)

    def writeComponentIntoParent(self, parentFs, fs, comp, parentElem):
        if comp.getLocalName():
            elem = self.writeComponentElement(comp, parentElem)
        else:
            elem = parentElem
            comp.writeInto(elem)
        self.writeComponents(parentFs, fs, comp, elem)

    def writeComponentElement(self, comp, elem):
        dom = elem.ownerDocument
        namespaceURI = comp.getNamespaceURI()
        prefix = x.makeNamespacePrefix(elem, namespaceURI, prefered_prefix=comp.mapNamespace(namespaceURI))
        subElem = dom.createElementNS(comp.getNamespaceURI(), '%s:%s' % (prefix, comp.getLocalName()) if prefix else comp.getLocalName())
        elem.appendChild(subElem)
        comp.writeInto(subElem)
        return subElem

    def writeComponents(self, parentFs, fs, comp, parentElem):
        compFs = fs.relativeFs(comp.getComponentsSubPath())
        for subComp in comp.getComponents():
            subFs, subName, parse = self.writeComponent(parentFs, compFs, subComp, parentElem)
            if subName and parse:
                subName = subFs.getRelativePathFrom(parentFs, subName)
                xi = x.makeNamespacePrefix(parentElem, XInclude_NS, prefered_prefix='xi')
                elem = parentElem.ownerDocument.createElementNS(XInclude_NS, '%s:include' % xi)
                elem.setAttributeNS(XInclude_NS, '%s:href' % xi, urllib.pathname2url(subName))
                elem.setAttributeNS(XInclude_NS, '%s:parse' % xi, parse)
                parentElem.appendChild(elem)
