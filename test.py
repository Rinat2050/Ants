import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.label = QLabel("Click in this window")
        self.setCentralWidget(self.label)
        button = QPushButton("Press Me!")
        button.clicked.connect(self.the_button_was_clicked)


    def the_button_was_clicked(self):
        print("Clicked!")

    def mouseMoveEvent(self, e):
        self.label.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        self.label.setText("mousePressEvent")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()