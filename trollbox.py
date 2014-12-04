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
        saveButton = QPushButton("Save Selection", centralWidget)
        deleteButton = QPushButton("Delete Selection", centralWidget)

        searchEdit = QLineEdit(centralWidget)
        searchEdit.setPlaceholderText("Image Tag Search")
        liveCheckBox = ClearableCheckBox("Keylogger Search", centralWidget)
        imagePicker = ImagePicker(centralWidget)

        getUrlEdit = QLineEdit(centralWidget)
        getUrlEdit.setPlaceholderText("Download Image URL")
        getUrlButton = QPushButton("Get URL", centralWidget)

        # Set layout
        layout = QGridLayout(centralWidget)
        layout.addWidget(imagePicker, 0, 0, 4, 19)
        selectionBox = QVBoxLayout()
        selectionBox.addWidget(self.urlEdit)
        selectionBox.addWidget(self.tagEdit)
        selectionBox.addWidget(saveButton)
        selectionBox.addWidget(deleteButton)
        layout.addLayout(selectionBox, 0, 20)
        layout.addWidget(searchEdit, 5, 0)
        layout.addWidget(liveCheckBox, 5, 1)
        layout.addWidget(getUrlEdit, 6, 0)
        layout.addWidget(getUrlButton, 6, 1)

        # Let user search by tag and URL
        #self.tagEdit.textChanged.connect(imagePicker.setFilterTagsString)
        #self.urlEdit.textChanged.connect(imagePicker.setFilterUrl)

        # When user picks an image, filter out others
        #imagePicker.selectedTagsStringChanged.connect(self.tagEdit.setText)
        #imagePicker.selectedUrlChanged.connect(self.urlEdit.setText)

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
