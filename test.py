#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    # from PyQt5 import QtCore, QtWidgets, QtGui
    from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow
    from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap, QPalette
    from PyQt5.QtCore import Qt
    import sys

    class MainWindow(QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi()

        def setupUi(self):
            self.setWindowTitle("Ants")  # заголовок окна
            self.move(1000, 100)  # положение окна
            self.resize(800, 800)  # размер окна

    class Example(QWidget):
        def __init__(self):
            super().__init__()

            self.initUI()

        def initUI(self):
            self.setGeometry(300, 300, 350, 100)
            self.setWindowTitle('Colours')
            self.show()

        def paintEvent(self, e):
            qp = QPainter()
            qp.begin(self)
            self.drawRectangles(qp)
            qp.end()

        def drawRectangles(self, qp):
            col = QColor(0, 0, 0)
            col.setNamedColor('#d4d4d4')
            qp.setPen(col)

            qp.setBrush(QColor(200, 0, 0))
            qp.drawRect(10, 15, 90, 60)

            qp.setBrush(QColor(255, 80, 0, 160))
            qp.drawRect(130, 15, 90, 60)

            qp.setBrush(QColor(25, 0, 90, 200))
            qp.drawRect(250, 15, 90, 60)

    class Hex_button(QPushButton):
        def __init__(self, window, coord_row, coord_column, HEX_WIDTH, HEX_HEIGHT):
            super().__init__()
            pixmap = QPixmap("image/hex_kompas.png").scaled(
                HEX_WIDTH, HEX_HEIGHT, Qt.KeepAspectRatio, Qt.FastTransformation)
            pal = self.palette()
            pal.setBrush(QPalette.Normal, QPalette.Button, QBrush(pixmap))
            pal.setBrush(QPalette.Inactive, QPalette.Button, QBrush(pixmap))
            self.setPalette(pal)
            self.row = 0
            self.column = 0
            self.button = QPushButton('text', window)
            self.button.setFixedSize(HEX_WIDTH, HEX_HEIGHT)
            self.button.move(coord_row, coord_column)
            # self.button.clicked.connect(QtWidgets.qApp.quit)
            self.button.setPalette(pal)
            self.button.setMask(pixmap.mask())
            self.offset = None
            self.installEventFilter(self)

        def set_text(self):
            pass

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        win = MainWindow()

        HEX_COORD_X = 50
        HEX_COORD_Y = 50
        HEX_WIDTH = 100
        HEX_HEIGHT = int(HEX_WIDTH * (3 ** 0.5 / 2))

        for j in range(8):
            for i in range(6):
                coord_row = int(HEX_COORD_X + HEX_WIDTH * (j * 3 / 4))
                coord_column = HEX_COORD_Y + i * HEX_HEIGHT
                if j % 2 == 0:
                    coord_column = int(HEX_COORD_Y + HEX_HEIGHT * (i - 0.5))
                hex_1 = Hex_button(win, coord_row, coord_column, HEX_WIDTH, HEX_HEIGHT)
                hex_1.row = i
                hex_1.column = j
                hex_1.button.setText(f"{hex_1.row};{hex_1.column}")
                print(i, j, hex_1.row, hex_1.column)
        ex = Example()
        win.show()
        sys.exit(app.exec_())

    def initUI(self):
        self.setGeometry(300, 300, 350, 100)
        self.setWindowTitle('Colours')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def drawRectangles(self, qp):
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)

        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(10, 15, 90, 60)

        qp.setBrush(QColor(255, 80, 0, 160))
        qp.drawRect(130, 15, 90, 60)

        qp.setBrush(QColor(25, 0, 90, 200))
        qp.drawRect(250, 15, 90, 60)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
