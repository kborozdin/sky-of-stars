__author__ = 'borozdin'


import os
import re
import geometry
import star


NUMBER_RE = r"[\sA-Z]*([-+\d\.]+)"
HMS_RE = NUMBER_RE + ":" + NUMBER_RE + ":" + NUMBER_RE
COORDINATES_RE = "^" + NUMBER_RE + HMS_RE * 2 + NUMBER_RE * 3 + r"\s*([:\w]+)"


def parse_angle(hours, minutes, seconds, coefficient):
    return (float(hours.replace(" ", "")) * coefficient +
            float(minutes.replace(" ", "")) / 60 * coefficient +
            float(seconds.replace(" ", "")) / 60 / 60 * coefficient)


def parse_color(color):
    for char in color:
        if char.isupper():
            return char
    raise Exception()


def get_constellation_name(path, file):
    with open(path + file[:file.index(".")] + ".htm") as text:
        occurrence = re.search(r"Catalog: (\w+)", text.read())
        return occurrence.group(1)


def format_coordinates(h1, m1, s1, h2, m2, s2):
    return "Alf: {}:{}:{}\nDel: {}:{}:{}".format(h1, m1, s1, h2, m2, s2)


def parse_stars3d(root_path):
    stars = []
    path = root_path + "txt/"

    for file in os.listdir(path):
        constellation_name = get_constellation_name(root_path, file)
        with open(path + file) as text:
            for occurrence in re.findall(
                    COORDINATES_RE, text.read(), re.MULTILINE):
                longitude = parse_angle(
                    occurrence[1], occurrence[2], occurrence[3], 15)
                latitude = parse_angle(
                    occurrence[4], occurrence[5], occurrence[6], 1)

                point3d = geometry.Vector3D.convert_from_spherical_coordinates(
                    latitude, longitude)
                brightness = float(occurrence[9].replace(" ", ""))
                color = parse_color(occurrence[10])
                tooltip = format_coordinates(
                    occurrence[1], occurrence[2], occurrence[3],
                    occurrence[4], occurrence[5], occurrence[6])

                stars.append(star.Star(
                    point3d, brightness, color, constellation_name, tooltip))

    return stars
