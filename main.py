import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap, QPalette, QPen, QColor
from PyQt5.QtCore import Qt, QSize

HEX_COORD_X = 50
HEX_COORD_Y = 50
HEX_WIDTH = 100
HEX_HEIGHT = int(HEX_WIDTH * (3 ** 0.5 / 2))

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        #self.initUI()й
    def initUI(self):
        self.setWindowTitle("Ants")  # заголовок окна
        self.move(1000, 100)  # положение окна
        self.resize(800, 800)  # размер окна

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q:
            ant2 = Ant(index_to_coord(4, 4))
            ant.move(5, 5)
            print("Press q")
        event.accept()



class Ant(QWidget):
    def __init__(self, indexes):
        super().__init__()
        self.ellipse_diameter = 30
        self.coord_row = indexes[1] + (HEX_WIDTH - self.ellipse_diameter)//2
        self.coord_column = indexes[0] + (HEX_HEIGHT - self.ellipse_diameter)//2


    def paintEvent(self, event):
        painter = QPainter(self)
        brush = QBrush(Qt.blue)
        painter.setBrush(brush)
        pen = QPen(Qt.black)
        painter.setPen(pen)
        painter.drawRect(50, 50, 100, 50)

        painter.setPen(QPen(QColor(0, 255, 0), 2, Qt.SolidLine))
        painter.drawEllipse(self.coord_row, self.coord_column, self.ellipse_diameter, self.ellipse_diameter)

    def move(self, x, y):
        self.coord_row = 10
        self.coord_column = 20



def index_to_coord(column, row):
    return matrix[row][column].coord_column, matrix[row][column].coord_row


class Hex_button(QPushButton):
    def __init__(self, window, coord_row, coord_column, HEX_WIDTH, HEX_HEIGHT):
        super().__init__()
        pixmap = QPixmap("image/hex_kompas.png").scaled(
            HEX_WIDTH, HEX_HEIGHT, Qt.KeepAspectRatio, Qt.FastTransformation)
        pal = self.palette()
        pal.setBrush(QPalette.Normal, QPalette.Button, QBrush(pixmap))
        pal.setBrush(QPalette.Inactive, QPalette.Button, QBrush(pixmap))
        self.setPalette(pal)
        self.coord_row = coord_row
        self.coord_column = coord_column
        self.row = 0
        self.column = 0
        self.button = QPushButton('text', window)
        self.button.setFixedSize(HEX_WIDTH, HEX_HEIGHT)
        self.button.move(self.coord_row, self.coord_column)
        #self.button.clicked.connect(QtWidgets.qApp.quit)
        self.button.setPalette(pal)
        self.button.setMask(pixmap.mask())
        self.offset = None
        self.installEventFilter(self)

    def set_text(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()


    matrix = []
    for i in range(8):
        sub_matrix = []
        for j in range(6):
            coord_row = int(HEX_COORD_X + HEX_WIDTH*(j*3/4))
            coord_column = HEX_COORD_Y + i*HEX_HEIGHT
            if j % 2 == 0:
                coord_column = int(HEX_COORD_Y + HEX_HEIGHT*(i-0.5))
            hex_1 = Hex_button(win, coord_row, coord_column, HEX_WIDTH, HEX_HEIGHT)
            hex_1.row = i
            hex_1.column = j
            hex_1.button.setText(f"{hex_1.column}:{hex_1.row}")
            #print(i, j, hex_1.row, hex_1.column)
            sub_matrix.append(hex_1)
        matrix.append(sub_matrix)

    ant = Ant(index_to_coord(3, 2))
    print(index_to_coord(5, 7))
    win.setCentralWidget(ant)
    win.show()
    sys.exit(app.exec_())










