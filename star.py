__author__ = 'borozdin'

from PyQt5 import QtGui


class Star:
    def __init__(self, point, brightness, color, constellation, tooltip):
        self.point = point
        self.brightness = brightness
        self.color = color
        self.constellation = constellation
        self.tooltip = tooltip

    def get_color(self, visible_brightness):
        if self.color == "O" or self.color == "B":
            return QtGui.QColor(0, visible_brightness / 2, visible_brightness)
        if self.color == "G" or self.color == "K":
            return QtGui.QColor(visible_brightness, visible_brightness, 0)
        if self.color == "M":
            return QtGui.QColor(visible_brightness, visible_brightness / 2, 0)
        return QtGui.QColor(
            visible_brightness, visible_brightness, visible_brightness)
