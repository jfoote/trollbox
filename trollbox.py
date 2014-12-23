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
        self.liveCheckBox = ClearableCheckBox("Wordlogger", centralWidget)
        self.clearSearchButton = QPushButton("Clear/Show All", centralWidget)
        self.imagePicker = ImagePicker(centralWidget)

        self.getUrlEdit = QLineEdit(centralWidget)
        self.getUrlEdit.setPlaceholderText("Download Image URL")
        self.getUrlButton = QPushButton("Download URL", centralWidget)
        self.pasteUrlButton = QPushButton("Paste to URL", centralWidget)

        # Set layout
        layout = QGridLayout(centralWidget)
        layout.addWidget(self.imagePicker, 0, 0, 3, 3)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)

        selectionBox = QVBoxLayout()
        selectionBox.addWidget(self.urlEdit)
        selectionBox.addWidget(self.tagEdit)
        selectionBox.addWidget(saveButton)
        selectionBox.addWidget(deleteButton)
        layout.addLayout(selectionBox, 0, 3, 1, 1)

        #searchBox = QHBoxLayout()
        #searchBox.addWidget(self.searchEdit)
        #searchBox.addWidget(self.clearSearchButton)
        #searchBox.addWidget(self.liveCheckBox)
        layout.addWidget(self.searchEdit, 5, 0, 1, 2)
        layout.addWidget(self.liveCheckBox, 5, 2, 1, 1)
        layout.addWidget(self.clearSearchButton, 5, 3, 1, 1)
        #layout.addLayout(searchBox, 5, 0, 1, 2)

        #urlBox = QHBoxLayout()
        #urlBox.addWidget(self.getUrlEdit)
        #urlBox.addWidget(self.getUrlButton)
        #urlBox.addWidget(self.pasteUrlButton)
        layout.addWidget(self.getUrlEdit, 6, 0, 1, 2)
        layout.addWidget(self.getUrlButton, 6, 2, 1, 1)
        layout.addWidget(self.pasteUrlButton, 6, 3, 1, 1)
        #layout.addLayout(urlBox, 6, 0, 1, 2)

        # Let user search by tag 
        self.searchEdit.textChanged.connect(self.imagePicker.setFilterTagsString)
        self.clearSearchButton.clicked.connect(self.clearSearch)

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
        self.getUrlButton.clicked.connect(self.downloadImage)
        self.pasteUrlButton.clicked.connect(self.pasteUrl)

        self.getUrlEdit.setText("https://avatars3.githubusercontent.com/u/2072203?v=3&s=460")

        # Enable wordlogging support
        self.wordlogger = get_wordlogger()
        self.liveCheckBox.stateChanged.connect(self.toggleWordLogging)

        # Enable fast URL copying (this might be annoying)
        self.imagePicker.clicked.connect(self.copyUrl)

        self.statusBar().showMessage("Click an image to copy its URL")

    def clearSearch(self):
        self.searchEdit.setText("")
        self.statusBar().showMessage("Cleared search")

    def copyUrl(self):
        if self.imagePicker.selectedIndexes():
            url = self.urlEdit.text()
            QApplication.clipboard().setText(url)
            print "copied URL to clipboard:", url
            self.statusBar().showMessage("Copied '%s'" % url)

    def pasteUrl(self):
        data = QApplication.clipboard().mimeData()
        if data.hasText():
            self.getUrlEdit.setText(data.text())
        else:
            self.statusBar().showMessage("Paste URL: No text on clipboard")
            print "Paste URL: No text on clipboard"
        self.statusBar().showMessage("Pasted URL")

    def toggleWordLogging(self, new_state):
        if (new_state == Qt.Checked) and not self.wordlogger.is_active():
            # clicking into UI elements disables live search 
            self.searchEdit.textEdited.connect(self.liveCheckBox.clear)
            self.urlEdit.textEdited.connect(self.liveCheckBox.clear)
            self.tagEdit.textEdited.connect(self.liveCheckBox.clear)
            self.getUrlEdit.textEdited.connect(self.liveCheckBox.clear)
            self.getUrlButton.clicked.connect(self.liveCheckBox.clear)
            self.pasteUrlButton.clicked.connect(self.liveCheckBox.clear)
            self.imagePicker.clicked.connect(self.liveCheckBox.clear)

            # start word logger thread
            self.wordlogger.start()
            self.wordlogger.wordEntered.connect(self.searchEdit.setText)
        else:
            # stop word logger thread
            self.wordlogger.stop()
            self.wordlogger.wordEntered.disconnect(self.searchEdit.setText)

            # disable connections to UI elements
            self.searchEdit.textEdited.disconnect(self.liveCheckBox.clear)
            self.urlEdit.textEdited.disconnect(self.liveCheckBox.clear)
            self.tagEdit.textEdited.disconnect(self.liveCheckBox.clear)
            self.getUrlEdit.textEdited.disconnect(self.liveCheckBox.clear)
            self.getUrlButton.clicked.disconnect(self.liveCheckBox.clear)
            self.pasteUrlButton.clicked.disconnect(self.liveCheckBox.clear)
            self.imagePicker.clicked.disconnect(self.liveCheckBox.clear)
        self.statusBar().showMessage("Toggled word logger")

    def downloadImage(self):
        downloader = ImageDownloader(self)
        downloader.failure.connect(self.showDownloadError)
        downloader.success.connect(self.imagePicker.addImage)
        downloader.success.connect(self.searchEdit.clear)
        url = self.getUrlEdit.text()
        downloader.get(url, self.imagePicker.getLocalFilepath(url))
        self.statusBar().showMessage("Downloading %s" % url)

    def showDownloadError(self, message):
        mb = QMessageBox()
        mb.setText(message)
        mb.exec_()
        
    def saveTags(self):
        self.imagePicker.setTagsString(self.tagEdit.text())
        self.statusBar().showMessage("Saved tags")

class ClearableCheckBox(QCheckBox):
    @Slot()
    def clear(self):
        self.setChecked(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
