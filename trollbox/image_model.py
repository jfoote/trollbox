import os, json

from PySide.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide.QtGui import QIcon

class ImageModel(QAbstractListModel):
    TagRole = 0x101
    
    def __init__(self, parent=None, troll_dir=None):
        QAbstractListModel.__init__(self, parent)

        # load data from disk
        default = os.path.expanduser(os.path.join("~", ".trollbox"))
        self.troll_dir = troll_dir if troll_dir else default
        if not os.path.exists(self.troll_dir):
            os.mkdir(self.troll_dir)
        self.metadata_path = os.path.join(self.troll_dir, "metadata.json")
        if os.path.exists(self.metadata_path):
            metadata = json.load(open(self.metadata_path, "rt"))
        else:
            metadata = []

        self.images = []
        for url, tags, local_path in metadata:
            self.images.append((url, tags, local_path, QIcon(local_path)))

    def image_dir(self):
        return os.path.join(self.troll_dir, "images")

    def image_path(self, filename):
        return os.path.join(self.image_dir(), filename)

    def rowCount(self, parent_index=None):
        if parent_index != None:
            i = parent_index.row()
        else:
            i = 0
        return len(self.images[i:])

    def addImage(self, url, tags, local_path):
        '''
        Adds an image with url and tags that has already been downloaded
        to local_path to the model.
        '''
        icon = QIcon(local_path)
        self.images.append((url, tags, local_path, icon))
        self.save()

    def save(self):
        json.dump([t[:3] for t in self.images], open(self.metadata_path, "wt"))

    def data(self, index, role=Qt.DisplayRole):
        """
        Returns the image data for role stored at index
        """
        url, tags, local_path, icon = self.images[index]
        if role == Qt.DecorationRole:
            return icon
        elif role == Qt.DisplayRole:
            return url
        elif role == self.TagRole:
            return tags

    def setData(self, index, value, role=Qt.DisplayRole):
        """
        Sets the role data for image stored at index to value
        """
        url, tags, local_path, icon = self.images[index]
        if role == Qt.DecorationRole:
            local_path = value
            icon = QIcon(local_path)
        elif role == Qt.DisplayRole:
            url = value
        elif role == self.TagRole:
            tags = value
        self.images[index] = url, tags, local_path, icon
