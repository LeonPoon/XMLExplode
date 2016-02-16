

from xmlxplode.xmlcomp import XmlComponent, CDataComponent

class DtsxComponent(XmlComponent):

    defaultNamespaceURI = 'www.microsoft.com/SqlServer/Dts'
    defaultPrefix = 'DTS'

    def __init__(self, *args, **kwargs):
        super(DtsxComponent, self).__init__(*args, **kwargs)
        self.mapNamespace(DtsxComponent.defaultNamespaceURI, DtsxComponent.defaultPrefix)
    
    def addComponentFromXmlCData(self, xml):
        props = self.getProperties()
        name = props.get((DtsxComponent.defaultNamespaceURI, 'Name')) or props.get((None, 'Name'))
        if name:
            name = name.rsplit('\\', 1)
            name.reverse()
            name = tuple(name.replace('\\', '/') for name in name)
        else:
            name = ()
        self.addComponentRaw(CDataComponent(xml.data, *name))

    def addComponentFromXml(self, xml):
        self.addComponentRaw(self.__class__(xml))
    
    def getFileName(self):
        return '%s.xml' % self.getLocalName()

    def getSubFolderName(self):
        return self.getLocalName()



from executable import Executable
