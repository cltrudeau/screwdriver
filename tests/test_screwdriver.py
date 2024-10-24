from unittest import TestCase

from screwdriver import (dynamic_load, camelcase_to_underscore, 
    rows_to_columns, list_to_rows, head_tail_middle, parse_link, pprint,
    DictObject)
from waelstow import capture_stdout

# =============================================================================

class TestUtils(TestCase):
    def test_dynamic_load(self):
        import os
        fn = dynamic_load('os.path.abspath')
        self.assertEqual(os.path.abspath, fn)

    def test_camelcase(self):
        pairs = [
            ('one', 'one'),
            ('one_two', 'oneTwo'),
            ('one_two', 'OneTwo'),
        ]

        for pair in pairs:
            self.assertEqual(pair[0], camelcase_to_underscore(pair[1]))

    def test_rows_to_cols(self):
        matrix = [ 
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
        ]

        expected = [ 
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
        ]

        self.assertEqual(expected, rows_to_columns(matrix))

    def test_list_to_rows(self):
        src = [1, 2, 3, 4, 5, 6, ]
        expected = [[1, 2, 3], [4, 5, 6], ]

        self.assertEqual(expected, list(list_to_rows(src, 3)))

        # check it handles a non even division
        src.append(7)
        expected.append([7,])
        self.assertEqual(expected, list(list_to_rows(src, 3)))

    def test_head_tail_middle(self):
        expected = None, [], None
        self.assertEqual(expected, head_tail_middle([]))

        expected = 1, [], None
        self.assertEqual(expected, head_tail_middle([1, ]))

        expected = 1, [], 2
        self.assertEqual(expected, head_tail_middle([1, 2, ]))

        expected = 1, [2, ], 3
        self.assertEqual(expected, head_tail_middle([1, 2, 3, ]))

        expected = 1, [2, 3, ], 4
        self.assertEqual(expected, head_tail_middle([1, 2, 3, 4, ]))


    def test_parse_link(self):
        url, text = parse_link('')
        self.assertEqual('', url)
        self.assertEqual('', text)

        url, text = parse_link('before <a href="/foo/bar.html">Stuff</a> after')
        self.assertEqual('/foo/bar.html', url)
        self.assertEqual('Stuff', text)

    def test_pprint(self):
        d = {
            'foo':'bar',
            'thing':3,
        }

        expected = """{\n    "foo": "bar",\n    "thing": 3\n}\n"""

        with capture_stdout() as output:
            pprint(d)

        self.assertEqual(expected, output.getvalue())

    def test_dictobj(self):
        d = {
            'x':1,
            'y':2,
        }

        o = DictObject(d)
        self.assertEqual(1, o.x)
        self.assertEqual(2, o.y)
