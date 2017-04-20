__author__ = 'borozdin'

import math
import star
import collections


EPSILON = 1e-9
BINARY_SEARCH_ITERATIONS = 20


def float_equal(first, second):
    return abs(first - second) < EPSILON


def fit_in_segment(value, left_border, right_border):
    if value < left_border:
        return left_border
    if value > right_border:
        return right_border
    return value


def map_value(value, from_left, from_right, to_left, to_right):
    from_delta = value - from_left
    to_delta = from_delta * (to_right - to_left) / (from_right - from_left)
    return to_left + to_delta


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2D(self.x * other, self.y * other)

    def __truediv__(self, other):
        if float_equal(other, 0):
            raise Exception()
        return Vector2D(self.x / other, self.y / other)

    def __mod__(self, other):
        return self.x * other.x + self.y * other.y

    def length(self):
        return math.sqrt(self % self)

    def distance_to(self, other):
        return (self - other).length()

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __str__(self):
        return self.__repr__()

    def set_length(self, other):
        if float_equal(self.length(), 0):
            if float_equal(other, 0):
                return Vector2D(0, 0)
            raise Exception()
        return self / self.length() * other

    def __eq__(self, other):
        return float_equal(self.x, other.x) and float_equal(self.y, other.y)


class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def convert_from_spherical_coordinates(latitude, longitude):
        latitude = math.radians(latitude)
        longitude = math.radians(longitude)

        return Vector3D(math.cos(latitude) * math.cos(longitude),
                        math.cos(latitude) * math.sin(longitude),
                        math.sin(latitude))

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.y * other.z - self.z * other.y,
                            self.z * other.x - self.x * other.z,
                            self.x * other.y - self.y * other.x)
        return Vector3D(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        if float_equal(other, 0):
            raise Exception()
        return Vector3D(self.x / other, self.y / other, self.z / other)

    def __mod__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def length(self):
        return math.sqrt(self % self)

    def length2(self):
        return self % self

    def distance_to(self, other):
        return (self - other).length()

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + \
               str(self.z) + ")"

    def __str__(self):
        return self.__repr__()

    def set_length(self, other):
        if float_equal(self.length(), 0):
            if float_equal(other, 0):
                return Vector3D(0, 0, 0)
            raise Exception()
        return self / self.length() * other

    def normalize(self):
        return self.set_length(1)

    def rotate_orthogonal(self, axis):
        return self * axis

    def rotate(self, angle, axis):
        normal = self.rotate_orthogonal(axis)
        return self * math.cos(angle) + normal * math.sin(angle)

    def __neg__(self):
        return Vector3D(-self.x, -self.y, -self.z)

    def __eq__(self, other):
        return (float_equal(self.x, other.x) and
                float_equal(self.y, other.y) and
                float_equal(self.z, other.z))


def get_intersection(line1, line2, surface1, surface2, surface3):
    volume1 = (surface1 - line1) * (surface2 - line1) % (surface3 - line1)
    volume2 = (surface2 - line2) * (surface1 - line2) % (surface3 - line2)
    volume = volume1 + volume2

    if float_equal(volume, 0):
        return None

    return line1 + (line2 - line1) * volume1 / volume


class ViewArea:
    def __init__(self, view_vector3d, rotation_vector3d, view_angle):
        self.view_vector3d = view_vector3d
        self.rotation_vector3d = rotation_vector3d
        self.view_angle = view_angle

    def project_point3d(self, point3d, cos_view_angle, sin_view_angle):
        view_vector3d = self.view_vector3d

        if point3d % view_vector3d < cos_view_angle:
            return None

        surface_point3d = view_vector3d * cos_view_angle
        view_radius = sin_view_angle

        direction_vector1 = self.rotation_vector3d
        direction_vector2 = view_vector3d * direction_vector1

        projected_point3d = get_intersection(
            point3d, Vector3D(0, 0, 0), surface_point3d,
            surface_point3d + direction_vector1,
            surface_point3d + direction_vector2)
        if projected_point3d is None:
            raise Exception()

        pointing_vector = projected_point3d - surface_point3d
        distance = pointing_vector.length2()
        if distance > view_radius ** 2:
            return None

        result_point = Vector2D(pointing_vector % direction_vector1,
                                pointing_vector % direction_vector2)
        return result_point / view_radius

    def move(self, delta_up, delta_right, delta_rotation, delta_view_angle):
        self.view_vector3d = self.view_vector3d.rotate(
            -delta_up, self.rotation_vector3d)

        # rotate right using composition of rotations
        self.rotation_vector3d = self.rotation_vector3d.rotate_orthogonal(
            self.view_vector3d)
        self.view_vector3d = self.view_vector3d.rotate(
            delta_right, self.rotation_vector3d)
        self.rotation_vector3d = -self.rotation_vector3d.rotate_orthogonal(
            self.view_vector3d)

        self.rotation_vector3d = self.rotation_vector3d.rotate(
            delta_rotation, self.view_vector3d)

        # normalize vectors to fight against precision errors
        self.view_vector3d = self.view_vector3d.normalize()
        self.rotation_vector3d = self.rotation_vector3d.normalize()

        self.view_angle = fit_in_segment(
            self.view_angle + delta_view_angle, 0.01, math.pi / 2 - 0.01)

    def get_brightness_threshold(self):
        return 3 / self.view_angle

    def get_zoom_step(self):
        return self.view_angle / 20

    def get_rotate_step(self):
        return self.view_angle / 20

    def __repr__(self):
        return "(" + str(self.view_vector3d) + ", " + \
               str(self.rotation_vector3d) + ", " + str(self.view_angle) + ")"

    def __str__(self):
        return self.__repr__()


def project_visible_points(stars3d, view_area, obligatory_constellation=None):
    projected_stars2d = []
    brightness_threshold = view_area.get_brightness_threshold()

    cos_view_angle = math.cos(view_area.view_angle)
    sin_view_angle = math.sin(view_area.view_angle)

    for star3d in stars3d:
        if star3d.brightness > brightness_threshold:
            continue

        point2d = view_area.project_point3d(
            star3d.point, cos_view_angle, sin_view_angle)
        if point2d is not None:
            projected_stars2d.append(star.Star(
                point2d, star3d.brightness, star3d.color,
                star3d.constellation, star3d.tooltip))
        elif obligatory_constellation == star3d.constellation:
            return None

    return projected_stars2d


def calculate_constellations_properties(stars3d):
    vector_sum = collections.defaultdict(lambda: Vector3D(0, 0, 0))
    radii = {}

    for star3d in stars3d:
        vector_sum[star3d.constellation] += star3d.point

    for key in vector_sum:
        vector_sum[key] = vector_sum[key].normalize()
        # left_border = 0
        # right_border = math.pi / 2
        #
        # for iteration in range(0, BINARY_SEARCH_ITERATIONS):
        # middle = (left_border + right_border) / 2
        # stars2d = project_visible_points(
        #         stars3d,
        #         ViewArea(vector_sum[key], Vector3D(0, 1, 0), middle),
        #         key)
        #
        #     if stars2d is None:
        #         left_border = middle
        #     else:
        #         right_border = middle
        #
        # radii[key] = right_border

    return vector_sum, radii
