import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt, QPoint


class HoneycombWidget(QWidget):
    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths

    def paintEvent(self, event):
        painter = QPainter(self)

        size = min(self.width(), self.height())
        spacing = 10
        hex_width = (size - 3 * spacing) / 2
        hex_height = (size - 2 * spacing) / 2

        y_offset = hex_height + spacing
        x_offset = hex_width + spacing

        for i in range(2):
            y = i * (hex_height + spacing)
            for j in range(3):
                x = j * (hex_width + 1.5 * spacing if i % 2 == 0 else hex_width + spacing)

                points = [QPoint(x + hex_width / 4, y), QPoint(x + 3 * hex_width / 4, y),
                          QPoint(x + hex_width, y + hex_height / 2), QPoint(x + 3 * hex_width / 4, y + hex_height),
                          QPoint(x + hex_width / 4, y + hex_height), QPoint(x, y + hex_height / 2)]

                painter.drawPolygon(*points)

                image = QPixmap(self.image_paths[i * 3 + j])
                painter.drawPixmap(x, y, hex_width, hex_height, image.scaled(hex_width, hex_height, Qt.KeepAspectRatio))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_paths = ["path_to_your_image1.jpg", "path_to_your_image2.jpg", "path_to_your_image3.jpg",
                   "path_to_your_image4.jpg", "path_to_your_image5.jpg", "path_to_your_image6.jpg"]
    widget = HoneycombWidget(image_paths)
    widget.setGeometry(100, 100, 500, 440)
    widget.show()
    sys.exit(app.exec_())