#!/usr/bin/env python

import sys
from functools import partial
import PySide
from PySide.QtGui import *
from PySide.QtCore import Slot, Qt

from trollbox.image_picker import ImagePicker
from trollbox.image_downloader import ImageDownloader
from trollbox.wordlogger import get_wordlogger

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

        self.searchEdit = QLineEdit(centralWidget)
        self.searchEdit.setPlaceholderText("Image Tag Search")
        self.liveCheckBox = ClearableCheckBox("Wordlogger Search", centralWidget)
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
        layout.addWidget(self.searchEdit, 5, 0)
        layout.addWidget(self.liveCheckBox, 5, 1)
        layout.addWidget(self.getUrlEdit, 6, 0)
        layout.addWidget(getUrlButton, 6, 1)

        # Let user search by tag and URL
        self.searchEdit.textChanged.connect(self.imagePicker.setFilterTagsString)

        # Reflect selection in tags and URL boxes
        self.imagePicker.selectedTagsStringChanged.connect(self.tagEdit.setText)
        self.imagePicker.selectedUrlChanged.connect(self.urlEdit.setText)

        # Enabling saving changes of tags to model
        saveButton.clicked.connect(self.saveTags)
        self.tagEdit.returnPressed.connect(saveButton.clicked)

        # Enable deleting selections from model
        deleteButton.clicked.connect(self.imagePicker.deleteSelected)
        self.imagePicker.preDelete.connect(self.tagEdit.clear)
        self.imagePicker.preDelete.connect(self.urlEdit.clear)
        #self.imagePicker.preDelete.connect(self.searchEdit.clear)

        # Set up image downloading
        getUrlButton.clicked.connect(self.downloadImage)

        self.getUrlEdit.setText("http://i1.kym-cdn.com/photos/images/facebook/000/390/538/deb.jpg")

        # Enable wordlogging support
        self.wordlogger = get_wordlogger()
        self.liveCheckBox.stateChanged.connect(self.toggleWordLogging)

    def toggleWordLogging(self, new_state):
        if (new_state == Qt.Checked) and not self.wordlogger.is_active():
            self.wordlogger.start()
        else:
            self.wordlogger.stop()

    def downloadImage(self):
        downloader = ImageDownloader(self)
        downloader.failure.connect(self.showDownloadError)
        downloader.success.connect(self.imagePicker.addImage)
        downloader.success.connect(self.searchEdit.clear)
        url = self.getUrlEdit.text()
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
