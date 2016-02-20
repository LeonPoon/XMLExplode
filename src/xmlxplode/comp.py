
class ComponentBase(object):
        
    def getFileName(self):
        return None

    def getXIncludeParseType(self):
        return 'xml'

    def writeInto(self, container):
        pass

    def getLocalName(self):
        return None

    def getComponents(self):
        return ()

    def getComponentSubPath(self):
        return '.'

    def getComponentsSubPath(self):
        return '.'

