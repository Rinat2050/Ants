#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QApplication


class Window(QWidget):
    def __init__(self):
        super().__init__()

        hbox = QHBoxLayout()
        hbox.addWidget(QPushButton(str(1)))
        hbox.addWidget(QPushButton(str(2)))
        hbox.addWidget(QPushButton(str(3)))
        hbox.addWidget(QPushButton(str(4)))
        hbox.addWidget(QPushButton(str(5)))
        self.setLayout(hbox)

        self.setWindowTitle('QHBoxLayout')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())