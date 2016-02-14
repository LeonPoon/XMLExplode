
from xmlxplode.xploder import Exploder
from pydtsxplode.dtsx_obj.executable import Executable


class DtsxExploder(Exploder):
    
    def rootElement(self, elem):
        return Executable(elem)
