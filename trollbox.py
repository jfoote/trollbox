#!/usr/bin/env python

import sys
from functools import partial
import PySide
from PySide.QtGui import *
from PySide.QtCore import Slot

from trollbox.image_picker import ImagePicker
from trollbox.image_downloader import ImageDownloader

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
        self.urlEdit.setDisabled(True)
        saveButton = QPushButton("Save Selection", centralWidget)
        deleteButton = QPushButton("Delete Selection", centralWidget)

        searchEdit = QLineEdit(centralWidget)
        searchEdit.setPlaceholderText("Image Tag Search")
        liveCheckBox = ClearableCheckBox("Keylogger Search", centralWidget)
        self.imagePicker = ImagePicker(centralWidget)

        self.getUrlEdit = QLineEdit(centralWidget)
        self.getUrlEdit.setPlaceholderText("Download Image URL")
        getUrlButton = QPushButton("Get URL", centralWidget)

        # Set layout
        layout = QGridLayout(centralWidget)
        layout.addWidget(self.imagePicker, 0, 0, 4, 19)
        selectionBox = QVBoxLayout()
        selectionBox.addWidget(self.urlEdit)
        selectionBox.addWidget(self.tagEdit)
        selectionBox.addWidget(saveButton)
        selectionBox.addWidget(deleteButton)
        layout.addLayout(selectionBox, 0, 20)
        layout.addWidget(searchEdit, 5, 0)
        layout.addWidget(liveCheckBox, 5, 1)
        layout.addWidget(self.getUrlEdit, 6, 0)
        layout.addWidget(getUrlButton, 6, 1)

        # Let user search by tag and URL
        searchEdit.textChanged.connect(self.imagePicker.setFilterTagsString)

        # Reflect selection in tags and URL boxes
        self.imagePicker.selectedTagsStringChanged.connect(self.tagEdit.setText)
        self.imagePicker.selectedUrlChanged.connect(self.urlEdit.setText)

        # Enabling saving changes of tags to model
        saveButton.clicked.connect(self.saveTags)
        self.tagEdit.returnPressed.connect(saveButton.clicked)

        # Enable deleting selections from model
        deleteButton.clicked.connect(self.imagePicker.deleteSelected)

        # Set up image downloading
        getUrlButton.clicked.connect(self.downloadImage)

        self.getUrlEdit.setText("http://www.baldhiker.com/wp-content/uploads/world.jpg") # TODO: delete

    def downloadImage(self):
        downloader = ImageDownloader(self)
        downloader.failure.connect(self.showDownloadError)
        url = self.getUrlEdit.text()
        print "downloading from ", url
        downloader.get(url, self.imagePicker.getLocalFilepath(url))

    def showDownloadError(self, message):
        mb = QMessageBox()
        mb.setText(message)
        mb.exec_()
        
    def saveTags(self):
        self.imagePicker.setTagsString(self.tagEdit.text())

class ClearableCheckBox(QCheckBox):
    @Slot()
    def clear(self):
        self.setChecked(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
