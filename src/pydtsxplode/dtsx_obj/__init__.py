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

from base64 import b64decode
from functools import partial
from xmlxplode.comp import ComponentBase
from xmlxplode.xmlcomp import XmlComponent, CDataComponent
import xmlxplode.simple_xml_utils as x


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



from executable import Executable

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
    (DtsxComponent.defaultNamespaceURI, 'Executable'): Executable,
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

