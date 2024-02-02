import sys
import math
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap, QPalette, QPen, QColor
from PyQt5.QtCore import Qt, QSize, QPoint

HEX_FIELD_X0 = 150
HEX_FIELD_Y0 = 150
# HEX_WIDTH = 100
# HEX_HEIGHT = int(HEX_WIDTH * (3 ** 0.5 / 2))
HEX_LENGTH = 50


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()  # параметры окна в отдельной функции
        layout = QVBoxLayout()  # Создаем вертикальный макет
        hex_field = HexField()
        layout.addWidget(hex_field)  # Добавляем "поле гексов" в макет
        self.setLayout(layout)  # Устанавливаем макет для главного окна

    def initUI(self):
        self.setWindowTitle("Ants")  # заголовок окна
        self.move(1000, 100)  # положение окна
        self.resize(800, 800)  # размер окна


class HexField(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()  # Создаем вертикальный макет
        # layout.setSpacing(0)
        # for i in range(5):
        #     hex = Hex(10, 10)
        #     hex.move(i*100, 50)
        #     layout.addWidget(hex)
        hex = Hex(22, 0)
        hex2 = Hex(0, 0)
        hex3 = Hex(50, 12)

        layout.addWidget(hex)
        layout.addWidget(hex2)
        layout.addWidget(hex3)
        self.setLayout(layout)  # Устанавливаем макет для виджета


class Hex(QWidget):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)  # сглаживание углов
        self.painter.setPen(QPen(Qt.green, 5, Qt.SolidLine))
        # self.painter.drawEllipse(self.x, self.y, 50, 100)
        self.painter.drawPolygon(hex_painting(self.x, self.y))


def hex_painting(center_x, center_y):
    coordinates = []
    for i in range(6):
        x = int(center_x + HEX_LENGTH * math.cos(i * 2 * math.pi / 6))
        y = int(center_y + HEX_LENGTH * math.sin(i * 2 * math.pi / 6))
        coordinates.append(QPoint(x, y))
    return coordinates


def index_to_coord(i, j):
    x = int(HEX_FIELD_X0 + i * math.cos(j * 2 * math.pi / 6))
    y = int(HEX_FIELD_Y0 + j * math.sin(j * 2 * math.pi / 6))
    return x, y


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
