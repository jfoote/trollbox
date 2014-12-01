from PySide.QtGui import *
from PySide.QtCore import QSize
from trollbox.image_model import ImageModel

class ImageSearcher(QSortFilterProxyModel):
    '''
    Supports filtering and sorting of images by tag.
    Note/hack: Uses "FilterRegExp" as a comma-separated list of tags.
    '''

    def __init__(self, parent=None):
        QSortFilterProxyModel.__init__(self, parent)
        self.filter_tags = []

    def lessThan(self, left_qmi, right_qmi):
        '''
        If data at left_qmi matches fewer tags than data at right_qmi returns
        True. Returns False otherwise.
        '''
        pass

    def setFilterTags(self, tags):
        '''
        Filters on tags (a list)
        '''
        self.filter_tags = tags
        self.setFilterRegExp("") # hack: triggers filter logic

    def filterAcceptsRow(self, row_index, parent_qmi):
        '''
        If data at row_index contains tags in self.filterRegEx() returns
        True. Returns False otherwise.
        '''
        
        # if no tags set, show all images
        if not self.filter_tags:
            return True

        qmi = self.sourceModel().index(row_index, 0, parent_qmi)
        tags = self.sourceModel().data(qmi, ImageModel.TagRole)
        intersection  = set(tags).intersection(set(self.filter_tags))
        return bool(intersection)

    def filterAcceptsColumn(*args, **kwargs):
        '''
        Model and view only have one column, so always return true.
        '''
        return True

class ImagePicker(QListView):
    def __init__(self, parent=None, model_path=None):
        QListView.__init__(self, parent)

        self.setViewMode(QListView.IconMode)
        self.setDragEnabled(False)
        self.setAcceptDrops(False)
        self.setIconSize(QSize(150,150))

        imageModel = ImageModel(parent, model_path)
        proxyModel = ImageSearcher(parent)
        proxyModel.setSourceModel(imageModel)
        self.setModel(proxyModel)

    def setFilterTags(self, *args, **kwargs):
        self.model().setFilterTags(*args, **kwargs)
