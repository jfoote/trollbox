import PySide
from PySide.QtGui import *
from PySide.QtCore import Signal, QObject, QUrl
from PySide.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class DownloadMessageBox(QMessageBox):
    '''
    The message box that gets displayed while a download is occurring.
    '''
    def __init__(self, *args, **kwargs):
        QMessageBox.__init__(self, *args, **kwargs)
        self.setText("Downloading...")
        self.setStandardButtons(QMessageBox.Cancel)
        self.setDefaultButton(QMessageBox.Cancel)

    def updateProgress(self, received, total):
        self.setText("Downloading %d/%d" % (received, total))

class ImageDownloader(QObject):
    '''
    Handles downloading images from supplied URLs. A DownloadMessageBox
    is shown while a respective download is occurring.
    '''
    # Signals
    success = Signal(str, str)
    failure = Signal(str)

    def __init__(self, parent, *args, **kwargs):
        QObject.__init__(self, parent, *args, **kwargs)
        self.mb = None

    def get(self, url, local_path):
        print "url", url
        print "local_path", local_path
        self.url = url
        self.local_path = local_path
        self.mb = DownloadMessageBox(self.parent())
        self.mb.buttonClicked.connect(self.handleCancel)
        self.mb.rejected.connect(self.handleReject)
        mgr = QNetworkAccessManager(self)
        mgr.finished.connect(self.handleFinished)
        self.reply = mgr.get(QNetworkRequest(QUrl(url)))
        self.reply.downloadProgress.connect(self.mb.updateProgress)
        self.mb.exec_()

    def handleCancel(self, button):
        print "cancel invoked"
        self.reply.abort()

    def handleReject(self):
        print "reject invoked"
        self.reply.abort()

    def handleFinished(self):
        code = self.reply.error()
        print "code is", code
        if code == QNetworkReply.NoError:
            open(self.local_path, "wb").write(self.reply.readAll())
            self.success.emit(self.url, self.local_path)
        else:
            self.failure.emit("Download failed. QT NetworkError code %d" % code)
        if self.mb:
            self.mb.accept()
            self.mb = None
        self.reply.deleteLater()

