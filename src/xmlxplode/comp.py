
class ComponentBase(object):
        
    def getFileName(self):
        return None

    def isWriteTextFile(self):
        return True

    def writeInto(self, container):
        pass

    def getLocalName(self):
        return None

    def getComponents(self):
        return ()

    def getSubFolderName(self):
        return '.'
