import unittest

from circle import area, perimeter


class CircleAreaTestCase(unittest.TestCase):
    def test_unit_radius(self):
        self.assertAlmostEqual(area(1), 3.14159265)

    def test_integer_radius(self):
        self.assertAlmostEqual(area(5), 78.5398163397)

    def test_fractional_radius(self):
        self.assertAlmostEqual(area(0.5), 0.7853981634)

    def test_zero_radius(self):
        self.assertEqual(area(0), 0)

    def test_big_radius(self):
        self.assertAlmostEqual(area(1000), 3141592.6535898)

    def test_string_radius(self):
        with self.assertRaises(TypeError):
            area('5')
    def test_negative_radius(self):
        with self.assertRaises(ValueError):
            area(-1)


class CirclePerimeterTestCase(unittest.TestCase):
    def test_unit_radius(self):
        self.assertAlmostEqual(perimeter(1), 6.2831853072)

    def test_integer_radius(self):
        self.assertAlmostEqual(perimeter(5), 31.4159265359)

    def test_fractional_radius(self):
        self.assertAlmostEqual(perimeter(2.5), 15.7079632679)

    def test_zero_radius(self):
        self.assertEqual(perimeter(0), 0)

    def test_string_radius(self):
        with self.assertRaises(TypeError):
            perimeter('5')

    def test_negative_radius(self):
        with self.assertRaises(ValueError):
            perimeter(-1)


if __name__ == '__main__':
    unittest.main()
