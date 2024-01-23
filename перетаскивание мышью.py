import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QColor, QMouseEvent
from PyQt5.QtCore import Qt



class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        label = DraggableLabel('Drag me!', self)
        label.setGeometry(100, 100, 100, 100)
        label.setStyleSheet('background-color: yellow')

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Draggable Object Example')
        self.show()

class DraggableLabel(QLabel):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        self.setMouseTracking(True)
        self.offset = None

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.offset is not None:
            self.move(self.mapToParent(event.pos() - self.offset))

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.offset = None



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())