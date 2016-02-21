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

