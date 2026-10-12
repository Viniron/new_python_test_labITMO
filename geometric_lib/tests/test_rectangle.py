import unittest

from rectangle import area, perimeter


class RectangleAreaTestCase(unittest.TestCase):
    def test_integer_sides(self):
        self.assertEqual(area(4, 5), 20)

    def test_zero_mul(self):
        self.assertEqual(area(10, 0), 0)

    def test_square_mul(self):
        self.assertEqual(area(10, 10), 100)

    def test_fractional_sides(self):
        self.assertAlmostEqual(area(2.5, 4), 10.0)

    # от перестановки сторон площадь меняться не должна
    def test_swap_sides(self):
        self.assertEqual(area(3, 7), area(7, 3))

    def test_string_side(self):
        with self.assertRaises(TypeError):
            area('4', 5)

    def test_negative_side(self):
        with self.assertRaises(ValueError):
            area(-4, 5)

    def test_both_negative_sides(self):
        with self.assertRaises(ValueError):
            area(-4, -5)


class RectanglePerimeterTestCase(unittest.TestCase):
    def test_integer_sides(self):
        self.assertEqual(perimeter(4, 5), 18)

    def test_square_sides(self):
        self.assertEqual(perimeter(10, 10), 40)

    def test_zero_sides(self):
        self.assertEqual(perimeter(0, 0), 0)

    # 0.1 + 0.2 во float не равно ровно 0.3, поэтому сравниваем приближённо
    def test_fractional_sides(self):
        self.assertAlmostEqual(perimeter(0.1, 0.2), 0.6)

    def test_swap_sides(self):
        self.assertEqual(perimeter(3, 7), perimeter(7, 3))

    def test_negative_side(self):
        with self.assertRaises(ValueError):
            perimeter(-4, 5)


if __name__ == '__main__':
    unittest.main()
