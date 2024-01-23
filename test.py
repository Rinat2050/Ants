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
        if event.key() == QtCore.Qt.Key_A:
            ant2 = Ant(index_to_coord(4, 4))
            ant.move(5, 5)
            print("Press a")
        event.accept()



class Ant(QWidget):
    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D:
            # ant2 = Ant(index_to_coord(4, 4))
            # ant.move(55, 55)
            print("Press d")
            #self.show()
        #event.accept()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    ant = Ant()
    ant.show()
    #app.installEventFilter(ant)
    win.show()
    sys.exit(app.exec_())










