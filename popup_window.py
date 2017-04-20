__author__ = 'borozdin'


from PyQt5 import QtCore, QtWidgets, QtGui


class PopupWindow(QtWidgets.QWidget):
    def __init__(self, text, coordinate_x, coordinate_y, is_hint, parent=None):
        super().__init__(parent)

        self.is_hint = is_hint

        self.setWindowFlags(QtCore.Qt.Popup)
        if is_hint:
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.move(coordinate_x, coordinate_y)

        label = QtWidgets.QLabel(text, self)
        if is_hint:
            label.setStyleSheet("QLabel { color: white }")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label)

    def keyPressEvent(self, event):
        #if self.is_hint:
        self.close()

    def mousePressEvent(self, event):
        #if self.is_hint:
        self.close()

    def wheelEvent(self, event):
        #if self.is_hint:
        self.close()
