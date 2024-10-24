__version__ = '0.15.0'

import json
from collections import namedtuple

from html.parser import HTMLParser

# =============================================================================
# Utility Methods
# =============================================================================

def dynamic_load(name):
    """Equivalent of "from X import Y" statement using dot notation to specify
    what to import and return.  For example, foo.bar.thing returns the item
    "thing" in the module "foo.bar" """
    pieces = name.split('.')
    item = pieces[-1]
    mod_name = '.'.join(pieces[:-1])

    mod = __import__(mod_name, globals(), locals(), [item])
    return getattr(mod, item)


def camelcase_to_underscore(text):
    prev_cap = text[0].isupper()
    result = [text[0].lower(), ]
    for letter in text[1:]:
        if letter.isupper():
            if not prev_cap:
                result.append('_')

            result.append(letter.lower())
            prev_cap = True
        else:
            result.append(letter)
            prev_cap = False

    return ''.join(result)


def pprint(data):
    """Alternative to `pprint.PrettyPrinter()` that uses `json.dumps()` for
    sorting and displaying data.

    :param data: item to print to STDOUT.  The item must be json serializable!
    """
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))


class DictObject(object):
    """Acts as a wrapper to a dictionary so that keys can be accessed as
    properties.

    >>> d = DictObject({'x'=1, 'y'=2})
    >>> d.x
    1
    >>> d._src
    {'x':1, 'y':2}
    """
    def __init__(self, src):
        self._src = src

    def __getattr__(self, name):
        return self._src[name]

# =============================================================================
# List Manipulation
# =============================================================================

def rows_to_columns(matrix):
    """Takes a two dimensional array and returns an new one where rows in the
    first become columns in the second."""
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    data = []
    for i in range(0, num_cols):
        data.append([matrix[j][i] for j in range(0, num_rows)])

    return data


def list_to_rows(src, size):
    """A generator that takes a enumerable item and returns a series of
    slices. Useful for turning a list into a series of rows.

    >>> list(list_to_rows([1, 2, 3, 4, 5, 6, 7], 3))
    [[1, 2, 3], [4, 5, 6], [7, ]]
    """

    row = []
    for item in src:
        row.append(item)
        if len(row) == size:
            yield row
            row = []

    if row:
        yield row


def head_tail_middle(src):
    """Returns a tuple consisting of the head of a enumerable, the middle
    as a list and the tail of the enumerable. If the enumerable is 1 item, the
    middle will be empty and the tail will be None.

    >>> head_tail_middle([1, 2, 3, 4])
    1, [2, 3], 4
    """

    if len(src) == 0:
        return None, [], None

    if len(src) == 1:
        return src[0], [], None

    if len(src) == 2:
        return src[0], [], src[1]

    return src[0], src[1:-1], src[-1]

# =============================================================================
# HTML Parsing
# =============================================================================

class AnchorParser(HTMLParser):
    ParsedLink = namedtuple('ParsedLink', ['url', 'text'])

    def __init__(self, *args, **kwargs):
        super(AnchorParser, self).__init__(*args, **kwargs)

        self.capture = 0
        self.url = ''
        self.text = ''

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            self.capture += 1

            if self.capture == 1:
                for attr in attrs:
                    if attr[0] == 'href':
                        self.url = attr[1]
                        break

    def handle_endtag(self, tag):
        if tag.lower() == 'a':
            self.capture += 1

    def handle_data(self, data):
        if self.capture == 1:
            self.text = data


def parse_link(html):
    """Parses an HTML anchor tag, returning the href and content text.  Any
    content before or after the anchor tag pair is ignored.

    :param html:
        Snippet of html to parse
    :returns:
        namedtuple('ParsedLink', ['url', 'text'])

    Example:

    .. code-block:: python

        >>> parse_link('things <a href="/foo/bar.html">Foo</a> stuff')
        ParsedLink('/foo/bar.html', 'Foo')
    """
    parser = AnchorParser()
    parser.feed(html)
    return parser.ParsedLink(parser.url, parser.text)
