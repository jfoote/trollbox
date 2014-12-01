from PySide.QtGui import *
from PySide.QtCore import QSize
from trollbox.image_model import ImageModel

class ImagePicker(QListView):
    def __init__(self, parent=0, model_path=None):
        QListView.__init__(self, parent)

        self.setViewMode(QListView.IconMode)
        self.setDragEnabled(False)
        self.setAcceptDrops(False)
        self.setIconSize(QSize(150,150))

        imageModel = ImageModel(parent, model_path)
        self.setModel(imageModel)
