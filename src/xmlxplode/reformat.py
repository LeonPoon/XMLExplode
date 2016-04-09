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



from collections import namedtuple
from os import linesep


Found = namedtuple('Found', 'pos, linePos, found')
WordSpec = namedtuple('WordSpec', 'word, len, index')
MatchLen = namedtuple('MatchLen', 'wordspec, len')

def reformat(x, sep=linesep):
    return ''.join(_reformat(x, len(x), 0, 0, sep))


def _prepare_lookups(*ks):
    return tuple(MatchLen(WordSpec(k, len(k), i), 0) for k, i in zip(ks, range(len(ks))))


def _find(x, l, pos, linePos, ks):
    d = list(ks)
    found = False
    while pos < l and d:
        c = x[pos]
        pos += 1
        linePos = 0 if c == '\r' or c == '\n' else linePos + 1
        i = len(d)
        while i > 0:
            i += -1
            t, v = d[i]
            k, kl, ki = t
            if k[v] == c:
                v += 1
                if v == kl:
                    if not found or kl > found.found.len:
                        found = Found(pos, linePos, t)
                    d[i] = ks[ki]
                else:
                    d[i] = (t, v)
            elif v > 0:
                d[i] = ks[ki]
        if found:
            d = [t for t in d if t[1]]
    return Found(found.pos, found.linePos, found.found.word) if found else Found(pos, linePos, False)


class _lines(list):

    def __init__(self):
        s = '                                                                                                        '
        for l in range(len(s)):
            self.append(s[:l])

    def __getitem__(self, item):
        l = len(self)
        while item >= l:
            self.append(self[l - 1] + ' ')
            l += 1
        return list.__getitem__(self, item)

_lines = _lines()


def _reformat(x, l, pos, linePos, sep):

    start = pos

    pos, linePos, found = _find(x, l, pos, linePos, _LOOKUP_PROLOG)
    if not found:
        yield x
        return

    lu = _LOOKUP_MISC
    attrLinePos = -1
    inAttr = False
    pos, linePos, found = _find(x, l, pos, linePos, lu)
    while found:
        #print pos, linePos, found, lu
        if found == '<':  # start of element
            attrLinePos = linePos
            hasAttr = False
            lu = _LOOKUP_INSIDE_ELEM
        elif found in ' \r\n\t':  # inside of element
            hasAttr = True
            yield x[start:pos-len(found)]
            start = pos
            yield sep
            yield _lines[attrLinePos]
            lu = _LOOKUP_ATTR
        elif found == '"' or found == "'":  # close of attr value
            if inAttr:
                inAttr = False
                lu = _LOOKUP_INSIDE_ELEM
            else:
                inAttr = True
                lu = _LOOKUP_ATTR_END_DOUBLE if found == '"' else _LOOKUP_ATTR_END_SINGLE
        elif found == '>' or found == '/>':  # end of element
            if hasAttr:
                hasAttr = False
                pos -= len(found)
                yield x[start:pos]
                start = pos
                yield sep
                yield _lines[attrLinePos]
            lu = _LOOKUP_MISC
        elif found == '<![CDATA[':
            lu = _LOOKUP_CDATA_END
        elif found == ']]>':
            lu = _LOOKUP_MISC
        elif found == '</':  # empty tag
            lu = _LOOKUP_DECL_END
        elif found == '<?':  # processing instruction
            lu = _LOOKUP_MISC_PI_END
        elif found == '?>':
            lu = _LOOKUP_MISC
        elif found == '<!':  # decl
            lu = _LOOKUP_DECL_END
        else:
            raise ValueError(found)
        pos, linePos, found = _find(x, l, pos, linePos, lu)

    yield x[start:pos]


_LOOKUP_PROLOG = _prepare_lookups('<?xml')
_LOOKUP_MISC = _prepare_lookups('<', '<![CDATA[', '<!--', '</', '<?', '<!')
_LOOKUP_CDATA_END = _prepare_lookups(']]>')
_LOOKUP_COMMENT_END = _prepare_lookups('-->')
_LOOKUP_MISC_PI_END = _prepare_lookups('?>')  # Processing instruction
_LOOKUP_DECL_END = _prepare_lookups('>')
_LOOKUP_INSIDE_ELEM = _prepare_lookups(' ', '\r', '\n', '\t', '>', '/>')
_LOOKUP_ATTR = _prepare_lookups('"', "'")
_LOOKUP_ATTR_END_DOUBLE = _prepare_lookups('"')
_LOOKUP_ATTR_END_SINGLE = _prepare_lookups("'")
