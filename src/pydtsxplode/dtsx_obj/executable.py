'''
Created on 14 Feb 2016

@author: szeleung
'''

from . import NamedDtsxComponent

class Executable(NamedDtsxComponent):
    '''
    classdocs
    '''

    
    def __init__(self, *args, **kwargs):
        super(Executable, self).__init__((NamedDtsxComponent.defaultNamespaceURI, 'ObjectName'), *args, **kwargs)
