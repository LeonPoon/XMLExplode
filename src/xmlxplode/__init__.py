# Copyright 2016 Leon Poon and Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
