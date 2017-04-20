__author__ = 'borozdin'

import unittest
from geometry import Vector2D, Vector3D, fit_in_segment, map_value, \
    get_intersection
import math


class TestGeometryUtilities(unittest.TestCase):
    def test_fit_in_segment(self):
        self.assertEqual(fit_in_segment(1, 2, 3), 2)
        self.assertEqual(fit_in_segment(2.5, 2, 3), 2.5)
        self.assertEqual(fit_in_segment(3, 2, 3), 3)
        self.assertEqual(fit_in_segment(4, 2, 3), 3)

    def test_map_value(self):
        self.assertEqual(map_value(1, 0, 4, 8, 10), 8.5)
        self.assertEqual(map_value(1, 0, 4, 10, 8), 9.5)
        self.assertEqual(map_value(2.5, 3, 2, 1, 2), 1.5)
        self.assertEqual(map_value(2.5, 3, 2, 2, 1), 1.5)


class TestVector2D(unittest.TestCase):
    def test_add(self):
        self.assertEqual(
            Vector2D(0, 0) + Vector2D(1, 1), Vector2D(1, 1))
        self.assertEqual(
            Vector2D(1, 0) + Vector2D(0, 2), Vector2D(1, 2))
        self.assertEqual(
            Vector2D(1, 2) + Vector2D(-2, -3), Vector2D(-1, -1))

    def test_sub(self):
        self.assertEqual(
            Vector2D(0, 0) - Vector2D(1, 1), Vector2D(-1, -1))
        self.assertEqual(
            Vector2D(1, 0) - Vector2D(0, 2), Vector2D(1, -2))
        self.assertEqual(
            Vector2D(1, 2) - Vector2D(-2, -3), Vector2D(3, 5))

    def test_mul(self):
        self.assertEqual(Vector2D(0, 0) * 2, Vector2D(0, 0))
        self.assertEqual(Vector2D(1, 0) * 3, Vector2D(3, 0))
        self.assertEqual(Vector2D(1, 2) * (-0.5), Vector2D(-0.5, -1))

    def test_div(self):
        self.assertEqual(Vector2D(0, 0) / 2, Vector2D(0, 0))
        self.assertEqual(Vector2D(1, 0) / 2, Vector2D(0.5, 0))
        self.assertEqual(Vector2D(1, 2) / (-0.5), Vector2D(-2, -4))
        self.assertRaises(Exception, Vector2D(1, 2).__truediv__, 1e-12)

    def test_scalar_product(self):
        self.assertEqual(Vector2D(0, 2) % Vector2D(2, 0), 0)
        self.assertEqual(Vector2D(2, 2) % Vector2D(-2, -2), -8)
        self.assertEqual(Vector2D(1, 3) % Vector2D(2, 4), 14)

    def test_length(self):
        self.assertEqual(Vector2D(0, 5).length(), 5)
        self.assertEqual(Vector2D(5, 5).length(), math.sqrt(50))
        self.assertEqual(Vector2D(-1, -1).length(), math.sqrt(2))

    def test_distance_to(self):
        self.assertEqual(
            Vector2D(0, 0).distance_to(Vector2D(1, 1)), math.sqrt(2))
        self.assertEqual(
            Vector2D(10, 10).distance_to(Vector2D(20, 10)), 10)
        self.assertEqual(
            Vector2D(-1, -1).distance_to(Vector2D(-2, -3)), math.sqrt(5))

    def test_set_length(self):
        self.assertEqual(
            Vector2D(1, 1).set_length(1),
            Vector2D(math.cos(math.pi / 4), math.sin(math.pi / 4)))
        self.assertEqual(
            Vector2D(0, 0).set_length(0), Vector2D(0, 0))
        self.assertRaises(Exception, Vector2D(0, 0).set_length, 1)


class TestVector3D(unittest.TestCase):
    def test_convert_from_spherical_coordinates(self):
        pass

    def test_add(self):
        self.assertEqual(
            Vector3D(0, 0, 0) + Vector3D(1, 1, 1), Vector3D(1, 1, 1))
        self.assertEqual(
            Vector3D(1, 0, 1) + Vector3D(0, 2, 0), Vector3D(1, 2, 1))
        self.assertEqual(
            Vector3D(1, 2, -3) + Vector3D(-2, -3, 3), Vector3D(-1, -1, 0))

    def test_sub(self):
        self.assertEqual(
            Vector3D(0, 0, 0) - Vector3D(1, 1, 1), Vector3D(-1, -1, -1))
        self.assertEqual(
            Vector3D(1, 0, 1) - Vector3D(0, 2, 0), Vector3D(1, -2, 1))
        self.assertEqual(
            Vector3D(1, 2, -3) - Vector3D(-2, -3, 3), Vector3D(3, 5, -6))

    def test_mul(self):
        self.assertEqual(Vector3D(0, 0, 0) * 2, Vector3D(0, 0, 0))
        self.assertEqual(Vector3D(1, 0, 2) * 3, Vector3D(3, 0, 6))
        self.assertEqual(Vector3D(1, 2, 3) * (-0.5), Vector3D(-0.5, -1, -1.5))

    def test_div(self):
        self.assertEqual(Vector3D(0, 0, 0) / 2, Vector3D(0, 0, 0))
        self.assertEqual(Vector3D(1, 0, 2) / 2, Vector3D(0.5, 0, 1))
        self.assertEqual(Vector3D(1, 2, 3) / (-0.5), Vector3D(-2, -4, -6))
        self.assertRaises(Exception, Vector3D(1, 2, 3).__truediv__, 1e-12)

    def test_scalar_product(self):
        self.assertEqual(Vector3D(0, 2, 0) % Vector3D(2, 0, 0), 0)
        self.assertEqual(Vector3D(2, 2, 2) % Vector3D(-2, -2, -2), -12)
        self.assertEqual(Vector3D(1, 3, 5) % Vector3D(2, 4, 6), 44)

    def test_vector_product(self):
        self.assertEqual(
            Vector3D(1, 2, 3) * Vector3D(4, 5, 6), Vector3D(-3, 6, -3))
        self.assertEqual(
            Vector3D(1, 0, 0) * Vector3D(0, 0, 1), Vector3D(0, -1, 0))
        self.assertEqual(
            Vector3D(-1, 2, -3) * Vector3D(2, -3, -4), Vector3D(-17, -10, -1))

    def test_length(self):
        self.assertEqual(Vector3D(0, 5, 0).length(), 5)
        self.assertEqual(Vector3D(5, 5, 5).length(), math.sqrt(75))
        self.assertEqual(Vector3D(-1, -1, -1).length(), math.sqrt(3))

    def test_length2(self):
        self.assertEqual(Vector3D(0, 5, 0).length2(), 25)
        self.assertEqual(Vector3D(5, 5, 5).length2(), 75)
        self.assertEqual(Vector3D(-1, -1, -1).length2(), 3)

    def test_distance_to(self):
        self.assertEqual(
            Vector3D(0, 0, 0).distance_to(Vector3D(1, 1, 1)), math.sqrt(3))
        self.assertEqual(
            Vector3D(10, 10, 10).distance_to(Vector3D(20, 10, 10)), 10)
        self.assertEqual(
            Vector3D(-1, -1, -1).distance_to(Vector3D(-2, -3, -4)),
            math.sqrt(14))

    def test_set_length(self):
        self.assertEqual(
            Vector3D(1, 1, 0).set_length(1),
            Vector3D(math.cos(math.pi / 4), math.sin(math.pi / 4), 0))
        self.assertEqual(
            Vector3D(0, 0, 0).set_length(0), Vector3D(0, 0, 0))
        self.assertRaises(Exception, Vector3D(0, 0, 0).set_length, 1)

    def test_normalize(self):
        self.assertEqual(
            Vector3D(1, 1, 0).normalize(),
            Vector3D(math.cos(math.pi / 4), math.sin(math.pi / 4), 0))
        self.assertEqual(
            Vector3D(2, 0, 0).normalize(), Vector3D(1, 0, 0))
        self.assertRaises(Exception, Vector3D(0, 0, 0).normalize)

    def test_rotate(self):
        self.assertEqual(
            Vector3D(0, 0, 1).rotate(math.pi, Vector3D(1, 0, 0)),
            Vector3D(0, 0, -1))
        self.assertEqual(
            Vector3D(-1, 0, 0).rotate(math.pi / 2, Vector3D(0, -1, 0)),
            Vector3D(0, 0, 1)
        )
        self.assertEqual(
            Vector3D(0, 2, 0).rotate(-math.pi / 4, Vector3D(1, 0, 0)),
            Vector3D(0, math.sqrt(2), math.sqrt(2))
        )

    def test_neg(self):
        self.assertEqual(
            -Vector3D(1, 1, 1), Vector3D(-1, -1, -1))
        self.assertEqual(
            -Vector3D(1, 0, -1), Vector3D(-1, 0, 1))
        self.assertEqual(
            -Vector3D(2, 5, -6), Vector3D(-2, -5, 6))


class TestIntersectionOfLineAndSurface(unittest.TestCase):
    def test_get_intersection(self):
        self.assertEqual(
            get_intersection(
                Vector3D(0, 0, 0), Vector3D(0, 0, 1), Vector3D(0, 0, 0),
                Vector3D(0, 1, 0), Vector3D(1, 0, 0)),
            Vector3D(0, 0, 0))
        self.assertIsNone(
            get_intersection(
                Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(0, 0, 0),
                Vector3D(0, 1, 0), Vector3D(1, 0, 0)))
        self.assertEqual(
            get_intersection(
                Vector3D(1, 1, 0), Vector3D(0, 0, 1), Vector3D(0, 0, 0),
                Vector3D(0, 1, 0), Vector3D(1, 0, 0)),
            Vector3D(1, 1, 0))


if __name__ == '__main__':
    unittest.main()
