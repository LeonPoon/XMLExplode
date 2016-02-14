'''
Created on 14 Feb 2016

@author: szeleung
'''

from . import DtsxComponent

class Executable(DtsxComponent):
    '''
    classdocs
    '''

    elemTagMap = {
                  }

    
    def getFileName(self):
        return 'Executable.xml'
