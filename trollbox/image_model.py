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
            abs_path = os.path.join(self.troll_dir, local_path)
            self.images.append((url, tags, local_path, abs_path, QIcon(abs_path)))

    def image_dir(self):
        return os.path.join(self.troll_dir, "images")

    def image_path(self, filename):
        return os.path.join(self.image_dir(), filename)

    def rowCount(self, parent_qmi=None):
        if parent_qmi != None:
            i = parent_qmi.row()
            if i == -1: # invalid index
                i = 0
        else:
            i = 0
        return len(self.images[i:])

    def addImage(self, url, tags, local_path):
        '''
        Adds an image with url and tags that has already been downloaded
        to local_path (relative to troll_dir) to the model.
        '''
        abs_path = os.path.join(self.troll_dir, local_path)
        icon = QIcon(abs_path)
        self.images.append((url, tags, local_path, abs_path, icon))
        self.save()

    def save(self):
        json.dump([t[:3] for t in self.images], open(self.metadata_path, "wt"))

    def data(self, qmi, role=Qt.DisplayRole):
        """
        Returns the image data for role stored at index
        """
        index = qmi.row()
        url, tags, local_path, abs_path, icon = self.images[index]
        if role == Qt.DecorationRole:
            return icon
        elif role == Qt.DisplayRole:
            return url
        elif role == self.TagRole:
            return tags

    def deleteImage(self, qmi):
        row = qmi.row()
        self.beginRemoveRows(qmi, row, row)
        _, _, local_path, abs_path, _ = self.images[row]
        del self.images[row]
        self.save()
        os.remove(abs_path)
        self.endRemoveRows()

    def setData(self, qmi, value, role=Qt.DisplayRole):
        """
        Sets the role data for image stored at index to value
        """
        index = qmi.row()
        url, tags, local_path, abs_path, icon = self.images[index]
        print "value", value
        if role == Qt.DisplayRole:
            url = value
        elif role == self.TagRole:
            tags = value
        self.images[index] = url, tags, local_path, abs_path, icon
        self.save()
        self.dataChanged.emit(qmi, qmi)
        return True
