import sys
import math
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap, QPalette, QPen, QColor
from PyQt5.QtCore import Qt, QSize, QPoint


HEX_COORD_X = 50
HEX_COORD_Y = 50
HEX_WIDTH = 100
HEX_HEIGHT = int(HEX_WIDTH * (3 ** 0.5 / 2))
HEX_LENGTH = 50


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()   # параметры окна в отдельной функции

    def initUI(self):
        self.setWindowTitle("Ants")  # заголовок окна
        self.move(1000, 100)  # положение окна
        self.resize(800, 800)  # размер окна
class Hex(QWidget):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.setPen(QPen(Qt.green, 5, Qt.SolidLine))
        self.painter.drawEllipse(self.x, self.y, HEX_WIDTH, HEX_HEIGHT)
        # self.painter.drawPolygon([
        #                         QPoint(self.x - HEX_LENGTH // 2, self.y - int(HEX_LENGTH * (3 ** 0.5 / 2))),
        #                         QPoint(self.x + HEX_LENGTH // 2, self.y - int(HEX_LENGTH * (3 ** 0.5 / 2))),
        #                         QPoint(self.x + HEX_LENGTH // 2, self.y - int(HEX_LENGTH * (3 ** 0.5 / 2))),
        #                         QPoint(self.x + HEX_LENGTH, self.y + int(HEX_LENGTH * (3 ** 0.5 / 2)))
        #           #                         ])
        self.painter.drawPolygon(hexagon_coordinates(HEX_LENGTH, self.x, self.y))


def hexagon_coordinates(s, center_x, center_y):
    coordinates = []
    for i in range(6):
        x = int(center_x + s * math.cos(i * 2 * math.pi / 6))
        y = int(center_y + s * math.sin(i * 2 * math.pi / 6))
        coordinates.append(QPoint(x, y))
    return coordinates





if __name__ == "__main__":
    print(hexagon_coordinates(100, 0, 0))
    app = QApplication(sys.argv)
    win = MyWindow()

    hex = Hex(200, 300)
    win.setCentralWidget(hex)

    #hex_field = Hex_field(3, 4)


    win.show()
    sys.exit(app.exec_())

