import unittest

from square import area, perimeter


class SquareAreaTestCase(unittest.TestCase):
    def test_integer_side(self):
        self.assertEqual(area(3), 9)

    def test_unit_side(self):
        self.assertEqual(area(1), 1)

    def test_fractional_side(self):
        self.assertAlmostEqual(area(2.5), 6.25)

    def test_zero_side(self):
        self.assertEqual(area(0), 0)

    def test_big_side(self):
        self.assertEqual(area(10 ** 6), 10 ** 12)

    def test_string_side(self):
        with self.assertRaises(TypeError):
            area('3')

    def test_negative_side(self):
        with self.assertRaises(ValueError):
            area(-3)


class SquarePerimeterTestCase(unittest.TestCase):
    def test_integer_side(self):
        self.assertEqual(perimeter(3), 12)

    def test_fractional_side(self):
        self.assertAlmostEqual(perimeter(2.5), 10.0)

    def test_zero_side(self):
        self.assertEqual(perimeter(0), 0)

    def test_big_side(self):
        self.assertEqual(perimeter(10 ** 6), 4 * 10 ** 6)

    def test_string_side(self):
        with self.assertRaises(TypeError):
            perimeter('3')

    def test_negative_side(self):
        with self.assertRaises(ValueError):
            perimeter(-3)


if __name__ == '__main__':
    unittest.main()
