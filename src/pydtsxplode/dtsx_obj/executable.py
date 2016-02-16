'''
Created on 14 Feb 2016

@author: szeleung
'''

from . import DtsxComponent

class Executable(DtsxComponent):
    '''
    classdocs
    '''

    
    def getFileName(self):
        return '%s.xml' % self.getLocalName()

    def addComponentFromXml(self, xml):
        self.addComponentRaw(DtsxComponent(xml))
    
    def getSubFolderName(self):
        return '.'
