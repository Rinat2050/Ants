import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Отдельное окно")
        self.setGeometry(100, 100, 300, 200)

class Shape(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        brush = QBrush(Qt.blue)
        painter.setBrush(brush)
        pen = QPen(Qt.black)
        painter.setPen(pen)
        painter.drawRect(50, 50, 100, 50)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    shape = Shape()
    window.setCentralWidget(shape)

    window.show()

    sys.exit(app.exec_())