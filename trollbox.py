#!/usr/bin/env python

import sys
import PySide
from PySide.QtGui import *

from trollbox.image_picker import ImagePicker

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.resize(800,600)
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        searchEdit = QLineEdit(centralWidget)
        tagEdit = QLineEdit(centralWidget)
        urlEdit = QLineEdit(centralWidget)
        liveCheckBox = QCheckBox("Live", centralWidget)
        copyButton = QPushButton("Copy URL", centralWidget)
        grabButton = QPushButton("Grab FireFox URL", centralWidget)
        imagePicker = ImagePicker(centralWidget)

        layout = QGridLayout(centralWidget)
        layout.addWidget(imagePicker, 0, 0, 2, 19)
        layout.addWidget(searchEdit, 20, 0)
        layout.addWidget(liveCheckBox, 20, 1)
        layout.addWidget(urlEdit, 21, 0)
        layout.addWidget(tagEdit, 21, 1)
        layout.addWidget(copyButton, 22, 0)
        layout.addWidget(grabButton, 22, 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
