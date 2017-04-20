__author__ = 'borozdin'


from PyQt5 import QtCore, QtWidgets


class SearchWindow(QtWidgets.QWidget):
    def __init__(self, text, words, update_function,
                 coordinate_x, coordinate_y, parent=None):
        super().__init__(parent)

        self.setWindowFlags(QtCore.Qt.Popup)
        self.move(coordinate_x, coordinate_y)

        layout = QtWidgets.QHBoxLayout(self)

        completer = QtWidgets.QCompleter(words, self)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.search_edit = QtWidgets.QLineEdit(text, self)
        self.search_edit.setCompleter(completer)
        self.search_edit.textChanged.connect(update_function)
        self.search_edit.setFocus()
        layout.addWidget(self.search_edit)

        self.clear_button = QtWidgets.QPushButton("X", self)
        self.clear_button.setFixedWidth(self.width() / 4)
        self.clear_button.clicked.connect(self.clear_button_pressed)
        layout.addWidget(self.clear_button)

        update_function(self.search_edit.text())

    def clear_button_pressed(self):
        self.search_edit.setText("")
        self.search_edit.setFocus()

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Return:
            self.close()
