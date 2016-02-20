
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
