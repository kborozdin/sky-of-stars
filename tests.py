__author__ = 'borozdin'

import math
import unittest
from geometry import Vector2D, Vector3D


class MyTestCase(unittest.TestCase):
    def test_2d(self):
        point = Vector2D(1, 1)
        point += Vector2D(2, 2)
        self.assertEqual(point, Vector2D(3, 3))
        self.assertEqual(point.length(), math.sqrt(18))
        point = point.set_length(math.sqrt(2))
        self.assertEqual(point, Vector2D(1, 1))

    def test_3d(self):
        point = Vector3D(1, 1, 1)
        point += Vector3D(2, 2, 2)
        self.assertEqual(point, Vector3D(3, 3, 3))
        self.assertEqual(point.length(), math.sqrt(27))
        point = point.set_length(math.sqrt(3))
        self.assertEqual(point, Vector3D(1, 1, 1))
        point -= Vector3D(0, 1, 1)
        point = point.rotate(math.pi, Vector3D(0, 1, 0))
        self.assertEqual(point, Vector3D(-1, 0, 0))

if __name__ == '__main__':
    unittest.main()
