#!/usr/bin/python3

__author__ = 'borozdin'

from PyQt5 import Qt, QtCore, QtGui, QtWidgets
import parser
import sys
import geometry
import popup_window
import search_window
import math


STAR_RADIUS = 2
CLICK_TOLERANCE = 5
STAR_SELECTION_RADIUS = STAR_RADIUS * 5

HELP_TEXT = (
    "<h3>Keyboard controls:</h3>"
    "<b>W</b> - rotate up<br>"
    "<b>S</b> - rotate down<br>"
    "<b>A</b> - rotate left<br>"
    "<b>D</b> - rotate right<br>"
    "<b>Q</b> - rotate counter-clockwise<br>"
    "<b>E</b> - rotate clockwise<br>"
    "<b>R</b> - zoom closer<br>"
    "<b>F</b> - zoom farther<br>"
    "<b>T</b> - clear selection<br>"
    "<h3>Mouse controls:</h3>"
    "<b>Left button + movement</b> - rotate up/down/left/right<br>"
    "<b>Wheel</b> - zoom closer/farther<br>"
    "<b>Right button</b> - select star under cursor and all its "
    "constellation<br>"
    "<b>Middle button</b> - show coordinates of star under cursor"
)

ABOUT_TEXT = (
    "<b>Kirill Borozdin</b><br>"
    "Thanks to Nikita Sivukhin and Alexey Danilyuk<br><br>"
    "<b>python.task, 2014</b>"
)


class Form(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stars3d = parser.parse_stars3d("stars/")
        self.view_area = geometry.ViewArea(geometry.Vector3D(0, 0, 1),
                                           geometry.Vector3D(0, 1, 0),
                                           math.pi / 5)
        self.stars2d = None
        self.update_stars2d()

        self.constellations_list = list(
            set([star.constellation for star in self.stars3d]))
        self.constellations_centers, self.constellations_radii = \
            geometry.calculate_constellations_properties(self.stars3d)

        self.mouse_press_coordinates = None
        self.selected_constellation = None

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.search_button = QtWidgets.QPushButton("Search", self)
        self.search_button.clicked.connect(self.show_search)
        layout.addWidget(self.search_button)
        self.search_text = ""

        self.help_button = QtWidgets.QPushButton("Help", self)
        self.help_button.clicked.connect(self.show_help)
        layout.addWidget(self.help_button)

        self.about_button = QtWidgets.QPushButton("About", self)
        self.about_button.clicked.connect(self.show_about)
        layout.addWidget(self.about_button)

        self.exit_button = QtWidgets.QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        self.info_popup = None

        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowTitle("Sky full of stars")
        self.background = QtGui.QImage("bg.png")

    def resizeEvent(self, event):
        width = self.width() / 10
        height = self.height() / 20

        self.help_button.setFixedSize(width, height)
        self.about_button.setFixedSize(width, height)
        self.search_button.setFixedSize(width, height)
        self.exit_button.setFixedSize(width, height)

    def show_help(self):
        position = self.help_button.mapToGlobal(Qt.QPoint(0, 0))
        help_form = popup_window.PopupWindow(
            HELP_TEXT,
            position.x(),
            position.y() + self.help_button.height(),
            False,
            self)
        help_form.show()

    def show_about(self):
        position = self.about_button.mapToGlobal(Qt.QPoint(0, 0))
        about_form = popup_window.PopupWindow(
            ABOUT_TEXT,
            position.x(),
            position.y() + self.about_button.height(),
            False,
            self)
        about_form.show()

    def show_search(self):
        position = self.search_button.mapToGlobal(Qt.QPoint(0, 0))
        search_form = search_window.SearchWindow(
            self.search_text,
            self.constellations_list,
            self.change_selected_constellation,
            position.x(),
            position.y() + self.about_button.height(),
            self)
        search_form.show()

    def show_info_popup(self, x, y, star):
        point2d = self.convert_point2d_to_screen_coordinates(star.point)
        text = star.tooltip

        self.info_popup = popup_window.PopupWindow(
            text,
            self.x() + point2d.x,
            self.y() + point2d.y,
            True,
            self)
        self.info_popup.show()

    def change_selected_constellation(self, constellation):
        self.search_text = constellation
        self.selected_constellation = constellation.title()
        if constellation.title() in self.constellations_centers:
            new_view_vector3d = self.constellations_centers[
                constellation.title()]
            # new_view_angle = self.constellations_radii[constellation.title()]
            new_view_angle = self.view_area.view_angle
            self.view_area = geometry.ViewArea(
                new_view_vector3d, self.view_area.rotation_vector3d,
                new_view_angle)
        self.update_stars2d()

    def get_radius_and_shifts(self):
        side = min(self.width(), self.height())
        shift_width = (self.width() - side) / 2
        shift_height = (self.height() - side) / 2
        return side, shift_width, shift_height

    def convert_point2d_to_screen_coordinates(self, point2d):
        side, shift_width, shift_height = self.get_radius_and_shifts()
        return geometry.Vector2D(
            shift_width + side / 2 + point2d.x * side / 2,
            shift_height + side / 2 + point2d.y * side / 2)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        side, shift_width, shift_height = self.get_radius_and_shifts()

        rectangle = QtCore.QRect(0, 0, self.width(), self.height())
        painter.drawImage(rectangle, self.background)

        painter.setPen(QtGui.QColor("black"))
        painter.setBrush(QtGui.QColor("black"))
        painter.drawEllipse(shift_width, shift_height, side, side)

        threshold = self.view_area.get_brightness_threshold()
        if not self.stars2d:
            max_brightness = 0
        else:
            max_brightness = min(
                [star2d.brightness for star2d in self.stars2d])

        for star2d in self.stars2d:
            visible_brightness = geometry.map_value(
                star2d.brightness, threshold, max_brightness, 50, 255)
            color_object = star2d.get_color(visible_brightness)

            painter.setPen(color_object)
            painter.setBrush(color_object)

            point2d = self.convert_point2d_to_screen_coordinates(star2d.point)
            painter.drawEllipse(
                point2d.x - STAR_RADIUS / 2, point2d.y - STAR_RADIUS / 2,
                STAR_RADIUS, STAR_RADIUS)

            if star2d.constellation == self.selected_constellation:
                painter.setPen(QtGui.QColor("red"))
                painter.setBrush(QtGui.QColor("transparent"))
                painter.drawRect(point2d.x - STAR_SELECTION_RADIUS / 2,
                                 point2d.y - STAR_SELECTION_RADIUS / 2,
                                 STAR_SELECTION_RADIUS, STAR_SELECTION_RADIUS)

        if self.selected_constellation in self.constellations_list:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(side / 20)
            painter.setFont(font)
            painter.drawText(shift_width + side / 4, shift_height + side / 8,
                             side / 2, side / 4,
                             QtCore.Qt.TextWordWrap | QtCore.Qt.AlignHCenter,
                             self.selected_constellation.title())

    def keyPressEvent(self, event):
        rotate_step = self.view_area.get_rotate_step()
        zoom_step = self.view_area.get_zoom_step()
        key = event.key()

        if key == QtCore.Qt.Key_W:
            self.view_area.move(rotate_step, 0, 0, 0)
        if key == QtCore.Qt.Key_S:
            self.view_area.move(-rotate_step, 0, 0, 0)
        if key == QtCore.Qt.Key_D:
            self.view_area.move(0, rotate_step, 0, 0)
        if key == QtCore.Qt.Key_A:
            self.view_area.move(0, -rotate_step, 0, 0)
        if key == QtCore.Qt.Key_Q:
            self.view_area.move(0, 0, -rotate_step, 0)
        if key == QtCore.Qt.Key_E:
            self.view_area.move(0, 0, rotate_step, 0)
        if key == QtCore.Qt.Key_F:
            self.view_area.move(0, 0, 0, zoom_step)
        if key == QtCore.Qt.Key_R:
            self.view_area.move(0, 0, 0, -zoom_step)
        if key == QtCore.Qt.Key_T:
            self.selected_constellation = None

        self.update_stars2d()

    def get_nearest_star(self, click_point):
        for star2d in self.stars2d:
            point2d = self.convert_point2d_to_screen_coordinates(star2d.point)
            if point2d.distance_to(
                    click_point) <= CLICK_TOLERANCE * STAR_RADIUS:
                return star2d

    def mousePressEvent(self, event):
        side, shift_width, shift_height = self.get_radius_and_shifts()
        click_point = geometry.Vector2D(event.x(), event.y())
        circle_center = geometry.Vector2D(
            shift_width + side / 2, shift_height + side / 2)
        if click_point.distance_to(circle_center) > side / 2:
            return

        button = event.button()

        if button == QtCore.Qt.LeftButton:
            self.mouse_press_coordinates = event.pos()
        if button == QtCore.Qt.RightButton:
            nearest_star = self.get_nearest_star(click_point)
            self.selected_constellation = (None if not nearest_star else
                                           nearest_star.constellation)
            self.update()
        if button == QtCore.Qt.MiddleButton:
            nearest_star = self.get_nearest_star(click_point)
            if nearest_star:
                self.show_info_popup(event.x(), event.y(), nearest_star)

    def mouseMoveEvent(self, event):
        if self.mouse_press_coordinates is None:
            return
        rotate_step = self.view_area.get_rotate_step()

        delta_x = event.x() - self.mouse_press_coordinates.x()
        delta_y = event.y() - self.mouse_press_coordinates.y()
        self.view_area.move(delta_y / self.width() * 30 * rotate_step,
                            -delta_x / self.height() * 30 * rotate_step, 0, 0)
        self.mouse_press_coordinates = event.pos()

        self.update_stars2d()

    def mouseReleaseEvent(self, event):
        self.mouse_press_coordinates = None

    def wheelEvent(self, event):
        zoom_step = self.view_area.get_zoom_step()

        self.view_area.move(0, 0, 0, -event.angleDelta().y() / 120 * zoom_step)
        self.update_stars2d()

    def update_stars2d(self):
        self.stars2d = geometry.project_visible_points(
            self.stars3d, self.view_area)
        self.update()


def main():
    application = QtWidgets.QApplication(sys.argv)

    form = Form()
    form.show()

    exit(application.exec())


if __name__ == "__main__":
    main()
