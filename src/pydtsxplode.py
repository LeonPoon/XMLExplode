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

from xmlxplode.xploder import Exploder


from base64 import b64decode
from functools import partial
from xmlxplode.xmlcomp import XmlComponent, CDataComponent
import xmlxplode.simple_xml_utils as x
from xmlxplode.fs.inmem import InMemFs
from StringIO import StringIO
from xmlxplode.reformat import reformat

class DtsxComponent(XmlComponent):

    defaultNamespaceURI = 'www.microsoft.com/SqlServer/Dts'
    defaultPrefix = 'DTS'
    msEncodingMapping = {
        'UTF16LE': 'UTF-16LE',
        }

    def __init__(self, *args, **kwargs):
        super(DtsxComponent, self).__init__(*args, **kwargs)
        self.mapNamespace(self.defaultNamespaceURI, self.defaultPrefix)

    def getComponentClass(self, xml):
        namespaceURI, _, localName = x.getNameWithNS(xml.namespaceURI, xml.prefix, xml.nodeName)
        componentClass = COMPONENT_CLASSES.get((namespaceURI, localName)) or DtsxComponent
        return componentClass
    
    def mapEncoding(self, msEncodingName):
        return self.msEncodingMapping.get(msEncodingName, msEncodingName)


class NamedDtsxComponent(DtsxComponent):
    
    def __init__(self, componentNameAttributeName, *args, **kwargs):
        self.componentNameAttributeName = componentNameAttributeName
        super(NamedDtsxComponent, self).__init__(*args, **kwargs)
    
    def getName(self):
        return self.getProperties().get(self.componentNameAttributeName)
    
    def getFileName(self):
        name = self.getName()
        return '%s.xml' % name if name else None
    
    def getComponentsSubPath(self):
        name = self.getName()
        return name if name else super(NamedDtsxComponent, self).getComponentsSubPath() 


class FileContainerDtsxComponent(NamedDtsxComponent):
    
    def __init__(self, *args, **kwargs):
        super(FileContainerDtsxComponent, self).__init__((None, 'Name'), *args, **kwargs)

    def getFileName(self):
        return None

    def getComponentsSubPath(self):
        return '.'
    
    def getCDataFileName(self):
        name = self.getName()
        if name:
            name = name.replace('\\', '/')
            name = name.rsplit('/', 1)
            name.reverse()
        else:
            name = ()
        return name
    
    def addComponentFromXmlCData(self, xml):
        name = self.getCDataFileName()
        encoding = self.mapEncoding(self.getProperties().get((None, 'Encoding'), xml.ownerDocument.encoding))
        self.addComponentRaw(CDataComponent(xml.data, *name, encoding=encoding))
    


class ContainerDtsxComponent(DtsxComponent):

    def getFileName(self):
        return '%s.xml' % self.getLocalName()
    
    def getComponentsSubPath(self):
        return self.getLocalName()


class BinaryCDataComponent(CDataComponent):

    def __init__(self, data, *args, **kwargs):
        super(BinaryCDataComponent, self).__init__(b64decode(data), *args, **kwargs)            

    def getXIncludeParseType(self):
        return None


class BinaryContainerComponent(FileContainerDtsxComponent):
    
    def addComponentFromXmlString(self, xml):
        self.addComponentRaw(BinaryCDataComponent(xml.data, *self.getCDataFileName()))



class FixedFileNameFileContainerDtsxComponent(FileContainerDtsxComponent):

    def __init__(self, *args, **kwargs):
        super(FixedFileNameFileContainerDtsxComponent, self).__init__(*args, **kwargs)
        
    def addComponentFromXmlCData(self, xml):
        self.addComponentRaw(CDataComponent(xml.data, fileName='%s.xml' % self.getLocalName()))




COMPONENT_CLASSES = {
    (DtsxComponent.defaultNamespaceURI, ''): None,
    (DtsxComponent.defaultNamespaceURI, 'ConnectionManagers'): ContainerDtsxComponent,
    (DtsxComponent.defaultNamespaceURI, 'ConnectionManager'): partial(NamedDtsxComponent, (DtsxComponent.defaultNamespaceURI, 'ObjectName')),
    (DtsxComponent.defaultNamespaceURI, 'PackageParameters'): ContainerDtsxComponent,
    (DtsxComponent.defaultNamespaceURI, 'PackageParameter'): partial(NamedDtsxComponent, (DtsxComponent.defaultNamespaceURI, 'ObjectName')),
    (DtsxComponent.defaultNamespaceURI, 'Variables'): ContainerDtsxComponent,
    (DtsxComponent.defaultNamespaceURI, 'Variable'): partial(NamedDtsxComponent, (DtsxComponent.defaultNamespaceURI, 'ObjectName')),
    (DtsxComponent.defaultNamespaceURI, 'EventHandlers'): ContainerDtsxComponent,
    (DtsxComponent.defaultNamespaceURI, 'EventHandler'): partial(NamedDtsxComponent, (DtsxComponent.defaultNamespaceURI, 'EventName')),
    (DtsxComponent.defaultNamespaceURI, 'Executables'): ContainerDtsxComponent,
    (DtsxComponent.defaultNamespaceURI, 'Executable'): partial(NamedDtsxComponent, (DtsxComponent.defaultNamespaceURI, 'ObjectName')),
    (DtsxComponent.defaultNamespaceURI, 'PrecedenceConstraints'): ContainerDtsxComponent,
    (DtsxComponent.defaultNamespaceURI, 'DesignTimeProperties'): FixedFileNameFileContainerDtsxComponent,
    (None, 'components'): ContainerDtsxComponent,
    (None, 'component'): partial(NamedDtsxComponent, (None, 'name')),
    (None, 'inputs'): ContainerDtsxComponent,
    (None, 'input'): partial(NamedDtsxComponent, (None, 'name')),
    (None, 'inputColumns'): ContainerDtsxComponent,
    (None, 'outputs'): ContainerDtsxComponent,
    (None, 'output'): partial(NamedDtsxComponent, (None, 'name')),
    (None, 'outputColumns'): ContainerDtsxComponent,
    (None, 'externalMetadataColumns'): ContainerDtsxComponent,
    (None, 'properties'): ContainerDtsxComponent,
    (None, 'connections'): ContainerDtsxComponent,
    (None, 'connection'): partial(NamedDtsxComponent, (None, 'name')),
    (None, 'ScriptProject'): partial(NamedDtsxComponent, (None, 'Name')),
    (None, 'ProjectItem'): FileContainerDtsxComponent,
    (None, 'BinaryItem'): BinaryContainerComponent,
}

Executable = COMPONENT_CLASSES[(DtsxComponent.defaultNamespaceURI, 'Executable')]



class DtsxExploder(Exploder):
    
    def rootElement(self, elem): 
        return Executable(elem)

    def writexml(self, dom, f, encoding):
        buf = StringIO()
        dom.writexml(buf, encoding=encoding)
        f.write(reformat(buf.getvalue(), self.eol))

def main((opts, (dtsxFile, targetDir))):
    import sys
    fs = InMemFs()
    if dtsxFile == '-':
        source = sys.stdin
    else:
        dtsxFile = open(dtsxFile, 'rb')
        try:
            source = dtsxFile.read()
        finally:
            dtsxFile.close()
    DtsxExploder.explode(source, fs)
    for f in fs.writeOut(targetDir, yieldFilenames=opts.get('verbose')):
        print f
        
    

def parseOpts(argv):
    cmd = argv[0]
    argv = argv[1:] # first arg is ourself
    import getopt
    optlist, args = getopt.getopt(argv, 'v', ['verbose'])
    opts = {}
    for o, a in optlist:  # @UnusedVariable
        if o in ('-v', '--verbose'):
            opts['verbose'] = True
        else:
            assert False, '%s: unrecognized option %r' % (cmd, o)
    return opts, args
              
    
if __name__ == '__main__':
    import sys
    main(parseOpts(sys.argv))
    




