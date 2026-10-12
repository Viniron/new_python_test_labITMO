import unittest

from triangle import area, perimeter


class TriangleAreaTestCase(unittest.TestCase):
    def test_integer_values(self):
        self.assertEqual(area(6, 4), 12)

    def test_odd_product(self):
        self.assertAlmostEqual(area(3, 5), 7.5)

    def test_fractional_values(self):
        self.assertAlmostEqual(area(2.5, 2), 2.5)

    def test_zero_height(self):
        self.assertEqual(area(5, 0), 0)

    def test_string_side(self):
        with self.assertRaises(TypeError):
            area('6', 4)

    def test_negative_side(self):
        with self.assertRaises(ValueError):
            area(-6, 4)


class TrianglePerimeterTestCase(unittest.TestCase):
    def test_right_triangle(self):
        self.assertEqual(perimeter(3, 4, 5), 12)

    def test_equilateral(self):
        self.assertEqual(perimeter(2, 2, 2), 6)

    def test_fractional_sides(self):
        self.assertAlmostEqual(perimeter(1.5, 2.5, 3), 7.0)

    def test_string_side(self):
        with self.assertRaises(TypeError):
            perimeter('3', 4, 5)

    def test_negative_side(self):
        with self.assertRaises(ValueError):
            perimeter(-3, 4, 5)

    # такого треугольника не существует: 1 + 2 < 10
    def test_impossible_triangle(self):
        with self.assertRaises(ValueError):
            perimeter(1, 2, 10)


if __name__ == '__main__':
    unittest.main()
