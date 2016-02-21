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

import codecs


BOM_MAP = {
    codecs.BOM_UTF8: 'utf8',
    codecs.BOM_UTF32_BE: 'UTF-32BE',
    codecs.BOM_UTF32_LE: 'UTF-32LE',
    codecs.BOM_UTF16_BE: 'UTF-16BE',
    codecs.BOM_UTF16_LE: 'UTF-16LE',
}

BOM_MAP = dict((b, codecs.lookup(n)) for b, n in BOM_MAP.iteritems())
BOM_LOOKUP = dict((c, b) for b, c in BOM_MAP.iteritems())
