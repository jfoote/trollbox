import os, json

from PySide.QtCore import QAbstractListModel

class ImageModel(QAbstractListModel):
    def __init__(self, parent=None, troll_dir=None):
        QAbstractListModel.__init__(self, parent)

        # load data from disk
        default = os.path.expanduser(os.path.join("~", ".trollbox"))
        self.troll_dir = troll_dir if troll_dir else default
        if not os.path.exists(self.troll_dir):
            os.mkdir(self.troll_dir)
        self.metadata_path = os.path.join(self.troll_dir, "metadata.json")
        if os.path.exists(self.metadata_path):
            self.images = json.load(open(self.metadata_path, "rt"))
        else:
            self.images = {}

    def image_dir(self):
        return os.path.join(self.troll_dir, "images")

    def image_path(self, filename):
        return os.path.join(self.image_dir(), filename)

    def rowCount(self, parent_index=None):
        return len(self.images.keys())

    def addImage(self, url, tags, local_path):
        '''
        Adds an image with url and tags that has already been downloaded
        to local_path to the model.
        '''
        self.images[url] = (tags, local_path)
        self.save()

    def save(self):
        json.dump(self.images, open(self.metadata_path, "wt"))

