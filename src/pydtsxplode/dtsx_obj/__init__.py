

from xmlxplode.xmlcomp import XmlComponent 

class DtsxComponent(XmlComponent):

    defaultNamespaceURI = 'www.microsoft.com/SqlServer/Dts'
    defaultPrefix = 'DTS'

    def __init__(self, *args, **kwargs):
        super(DtsxComponent, self).__init__(*args, **kwargs)
        self.mapNamespace(DtsxComponent.defaultNamespaceURI, DtsxComponent.defaultPrefix)
    





from executable import Executable
