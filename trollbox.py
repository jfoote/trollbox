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
        searchEdit.setPlaceholderText("Search")
        tagEdit = QLineEdit(centralWidget)
        tagEdit.setPlaceholderText("Current Image Tags")
        urlEdit = QLineEdit(centralWidget)
        urlEdit.setPlaceholderText("Current Image URL")
        liveCheckBox = QCheckBox("Live", centralWidget)
        copyButton = QPushButton("Copy URL", centralWidget)
        grabButton = QPushButton("Grab FireFox URL", centralWidget)
        imagePicker = ImagePicker(centralWidget)

        # Bind search box to image picker contents
        searchEdit.textChanged.connect(imagePicker.setFilterTagsString)

        # Bind edit boxes to image picker selection
        # 1. reflect changes in imagePicker in edit boxes
        imagePicker.tagsStringChanged.connect(tagEdit.setText)
        imagePicker.urlChanged.connect(urlEdit.setText)
        # 2. clear selection when searching
        searchEdit.textChanged.connect(urlEdit.clear)
        searchEdit.textChanged.connect(tagEdit.clear)

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
