#!/usr/bin/env python

import sys
from functools import partial
import PySide
from PySide.QtGui import *
from PySide.QtCore import Slot

from trollbox.image_picker import ImagePicker

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.resize(800,600)
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        tagSearchEdit = QLineEdit(centralWidget)
        tagSearchEdit.setPlaceholderText("Search by Tag")
        urlSearchEdit = QLineEdit(centralWidget)
        urlSearchEdit.setPlaceholderText("Search by URL")
        tagEdit = QLineEdit(centralWidget)
        tagEdit.setPlaceholderText("Current Image Tags")
        urlEdit = QLineEdit(centralWidget)
        urlEdit.setPlaceholderText("Current Image URL")
        liveCheckBox = ClearableCheckBox("Live Tag Search", centralWidget)
        downloadButton = QPushButton("Get Search URL", centralWidget)
        deleteButton = QPushButton("Delete Current Image", centralWidget)
        imagePicker = ImagePicker(centralWidget)

        # Bind search box to image picker contents
        tagSearchEdit.textChanged.connect(imagePicker.setFilterTagsString)
        urlSearchEdit.textChanged.connect(imagePicker.setFilterUrl)

        # Bind edit boxes to image picker selection
        # - reflect changes from imagePicker in edit boxes
        imagePicker.tagsStringChanged.connect(tagEdit.setText)
        imagePicker.urlChanged.connect(urlEdit.setText)
        # - save changes to tag edit box in model
        tagEdit.textEdited.connect(imagePicker.setTagsString)
        tagEdit.textEdited.connect(tagSearchEdit.clear)

        layout = QGridLayout(centralWidget)
        layout.addWidget(imagePicker, 0, 0, 2, 19)
        layout.addWidget(urlEdit, 20, 0)
        layout.addWidget(tagEdit, 20, 1)
        layout.addWidget(deleteButton, 20, 2)
        layout.addWidget(tagSearchEdit, 21, 0)
        layout.addWidget(liveCheckBox, 21, 1)
        layout.addWidget(urlSearchEdit, 22, 0)
        layout.addWidget(downloadButton, 22, 1)

class ClearableCheckBox(QCheckBox):
    @Slot()
    def clear(self):
        self.setChecked(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
