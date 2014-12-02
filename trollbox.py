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

        # Define widgets
        self.tagEdit = QLineEdit(centralWidget)
        self.tagEdit.setPlaceholderText("Current Image Tags")
        self.urlEdit = QLineEdit(centralWidget)
        self.urlEdit.setPlaceholderText("Current Image URL")
        liveCheckBox = ClearableCheckBox("Live Tag Search", centralWidget)
        saveButton = QPushButton("Download/Save Changes", centralWidget)
        deleteButton = QPushButton("Delete Image", centralWidget)
        clearButton = QPushButton("Clear Searches", centralWidget)
        imagePicker = ImagePicker(centralWidget)

        # Set layout
        layout = QGridLayout(centralWidget)
        layout.addWidget(imagePicker, 0, 0, 2, 19)
        layout.addWidget(self.urlEdit, 20, 0)
        layout.addWidget(self.tagEdit, 20, 1)
        layout.addWidget(liveCheckBox, 20, 2)
        layout.addWidget(saveButton, 21, 0)
        layout.addWidget(clearButton, 21, 1)
        layout.addWidget(deleteButton, 21, 2)

        # Let user search by tag and URL
        self.tagEdit.textChanged.connect(imagePicker.setFilterTagsString)
        self.urlEdit.textChanged.connect(imagePicker.setFilterUrl)

        # When user picks an image, filter out others
        imagePicker.selectedTagsStringChanged.connect(self.tagEdit.setText)
        imagePicker.selectedUrlChanged.connect(self.urlEdit.setText)

        # - save changes to tag edit box in model
        #self.tagEdit.textEdited.connect(imagePicker.setTagsString)
        #self.tagEdit.textEdited.connect(tagSearchEdit.clear)

class ClearableCheckBox(QCheckBox):
    @Slot()
    def clear(self):
        self.setChecked(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
