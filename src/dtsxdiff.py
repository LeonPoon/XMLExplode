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
import difflib
import os, sys
from collections import namedtuple
from functools import partial

from pydtsxplode import DtsxExploder
from xmlxplode.fs.inmem import InMemFs


class DtsxExploderForDiff(DtsxExploder):
    pass


def getSource(filename):
    if filename == '-':
        source = sys.stdin
    else:
        dtsxFile = open(filename, 'rb')
        try:
            source = dtsxFile.read()
        finally:
            dtsxFile.close()
    return filename, source



def printDiff(diffObj, out=sys.stdout, sep=os.sep, linesep=os.linesep):
    l, r = diffObj
    if not l or not r:
        x, _ = l or r
        out.write('Only in %s: %s' % (sep.join(x[:-1]), x[-1]))
        out.write(linesep)
    else:
        (l, (tl, s1)), (r, (tr, s2)) = diffObj
        l = sep.join(l)
        r = sep.join(r)
        if tl != tr:
            out.write('File %s is %s while file %s is %s' % (l, tl, r, tr))
            out.write(linesep)
        else:
            s1 = reduce(lambda x, y: x + [y+'\n'], s1.split('\n'), [])
            s2 = reduce(lambda x, y: x + [y+'\n'], s2.split('\n'), [])
            map(out.write, difflib.unified_diff(s1, s2, l, r))



Diff = namedtuple('Diff', 'left, right')
DiffComp = namedtuple('DiffComp', 'parts, inf')
DiffInfo = namedtuple('DiffInfo', 'type, content')



def findDiffs(fn1, fs1, fn2, fs2):
    diffs = []
    names = [(n, (fs1.nodeType(n), fs2.nodeType(n))) for n in set(fs1.keys()).union(fs2.keys())]
    names.sort()
    for name, (l, r) in names:
        if l == r:
            if l == 'a regular file':
                l = DiffInfo(l, fs1[name])
                r = DiffInfo(r, fs2[name])
                if l != r:
                    name = [name]
                    diffs.append(Diff(DiffComp(fn1+name, l), DiffComp(fn2+name, r)))
            elif l == 'a directory':
                diffs = diffs + findDiffs(fn1 + [name], fs1[name], fn2 + [name], fs2[name])
            else:
                raise ValueError(l)
        else:
            name = [name]
            if not l:
                diffs.append(Diff(None, DiffComp(fn2 + name, DiffInfo(r, None))))
            elif not r:
                diffs.append(Diff(DiffComp(fn1 + name, DiffInfo(l, None)), None))
            else:  # not same type
                diffs.append(Diff(DiffComp(fn1 + name, DiffInfo(l, None)), DiffComp(fn2 + name, DiffInfo(r, None))))
    return diffs



def main((opts, (source1, source2)), out=sys.stdout):
    fn1, source1 = getSource(source1)
    fn2, source2 = getSource(source2)
    if source1 != source2:
        fs1 = InMemFs()
        DtsxExploderForDiff.explode(source1, fs1, dtsxName='Package')
        fs2 = InMemFs()
        DtsxExploderForDiff.explode(source2, fs2, dtsxName='Package')
        map(partial(printDiff, out=out), findDiffs([fn1], fs1, [fn2], fs2))



def parseOpts(argv):
    cmd = argv[0]
    argv = argv[1:] # first arg is ourself
    import getopt
    optlist, args = getopt.getopt(argv, '', [])
    opts = {}
    for o, a in optlist:  # @UnusedVariable
        assert False, '%s: unrecognized option %r' % (cmd, o)
    return opts, args


if __name__ == '__main__':
    import sys
    main(parseOpts(sys.argv))
