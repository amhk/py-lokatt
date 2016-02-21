import unittest

from ctrl import Buffer


class TestCase(unittest.TestCase):
    def test_buffer_split_range_anchor_top(self):
        buf = Buffer(None)
        values = range(1, 101)  # 1 2 3 .. 99 100

        # positive lineno
        expected = (1, )
        actual = buf._split_range(values, 1, 1, 'top')
        self.assertSequenceEqual(expected, actual)

        expected = (1, 2, 3)
        actual = buf._split_range(values, 3, 1, 'top')
        self.assertSequenceEqual(expected, actual)

        expected = (10, 11, 12)
        actual = buf._split_range(values, 3, 10, 'top')
        self.assertSequenceEqual(expected, actual)

        expected = (98, 99, 100)
        actual = buf._split_range(values, 3, 98, 'top')
        self.assertSequenceEqual(expected, actual)

        expected = (98, 99, 100)
        actual = buf._split_range(values, 300, 98, 'top')
        self.assertSequenceEqual(expected, actual)

        # negative lineno
        expected = (100, )
        actual = buf._split_range(values, 1, -1, 'top')
        self.assertSequenceEqual(expected, actual)

        expected = (100, )
        actual = buf._split_range(values, 3, -1, 'top')
        self.assertSequenceEqual(expected, actual)

        expected = (98, 99, 100)
        actual = buf._split_range(values, 3, -3, 'top')
        self.assertSequenceEqual(expected, actual)

        expected = (91, 92, 93)
        actual = buf._split_range(values, 3, -10, 'top')
        self.assertSequenceEqual(expected, actual)

    def test_buffer_split_range_anchor_middle(self):
        buf = Buffer(None)
        values = range(1, 101)  # 1 2 3 .. 99 100

        # positive lineno
        expected = (1, )
        actual = buf._split_range(values, 1, 1, 'middle')
        self.assertSequenceEqual(expected, actual)

        expected = (10, )
        actual = buf._split_range(values, 1, 10, 'middle')
        self.assertSequenceEqual(expected, actual)

        expected = (10, 11)
        actual = buf._split_range(values, 2, 10, 'middle')
        self.assertSequenceEqual(expected, actual)

        expected = (9, 10, 11)
        actual = buf._split_range(values, 3, 10, 'middle')
        self.assertSequenceEqual(expected, actual)

        expected = (9, 10, 11, 12)
        actual = buf._split_range(values, 4, 10, 'middle')
        self.assertSequenceEqual(expected, actual)

        expected = (8, 9, 10, 11, 12)
        actual = buf._split_range(values, 5, 10, 'middle')
        self.assertSequenceEqual(expected, actual)

        # negative lineno
        expected = (89, 90, 91, 92, 93)
        actual = buf._split_range(values, 5, -10, 'middle')
        self.assertSequenceEqual(expected, actual)

    def test_buffer_split_range_anchor_bottom(self):
        buf = Buffer(None)
        values = range(1, 101)  # 1 2 3 .. 99 100

        # positive lineno
        expected = (1, )
        actual = buf._split_range(values, 1, 1, 'bottom')
        self.assertSequenceEqual(expected, actual)

        expected = (3, 4, 5)
        actual = buf._split_range(values, 3, 5, 'bottom')
        self.assertSequenceEqual(expected, actual)

        expected = (16, 17, 18, 19, 20)
        actual = buf._split_range(values, 5, 20, 'bottom')
        self.assertSequenceEqual(expected, actual)

        expected = (1, 2, 3)
        actual = buf._split_range(values, 5, 3, 'bottom')
        self.assertSequenceEqual(expected, actual)

        # negative lineno
        expected = (100, )
        actual = buf._split_range(values, 1, -1, 'bottom')
        self.assertSequenceEqual(expected, actual)

        expected = (98, 99, 100)
        actual = buf._split_range(values, 3, -1, 'bottom')
        self.assertSequenceEqual(expected, actual)

        expected = (79, 80, 81)
        actual = buf._split_range(values, 3, -20, 'bottom')
        self.assertSequenceEqual(expected, actual)
