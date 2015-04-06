try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from chardet import detect
from lxml.html import parse, HTMLParser
from libextract.coretools import highest_scoring


NODES_WITH_TEXT = '//*[not(self::script or self::style)]/text()/..'
TEXT_IN_NODE = './/text()[normalize-space()]'

FILTER_TEXT = './/*[not(self::script or self::style or \
        self::figure or self::span or self::time)]/\
        text()[normalize-space()]'


def node_text_length(node):
    """
    Returns the length of the text contained within
    a given *node*.
    """
    return len(''.join(node.xpath(TEXT_IN_NODE)))


def get_etree(document):
    """
    Get an ElementTree instance from a given XML/HTML
    *document*. The encoding is automatically detected.
    """
    return parse(BytesIO(document),
                 HTMLParser(encoding=detect(document)['encoding'],
                            remove_blank_text=True))


def get_pairs(etree):
    """
    Given an *etree*, returns an iterable of parent
    to node text length pairs.
    """
    for node in etree.xpath(NODES_WITH_TEXT):
        yield node.getparent(), node_text_length(node)


def get_final_text(node):
    """
    Gets the text contained within the children node
    of a given *node*, joined by a space.
    """
    return ' '.join(node.xpath(FILTER_TEXT))


STRATEGY = (get_etree, get_pairs, highest_scoring, get_final_text)
