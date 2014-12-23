from PySide.QtGui import *
from PySide.QtCore import QSize, Qt, Signal, Slot, QModelIndex
from trollbox.image_model import ImageModel

class ImageSearcher(QSortFilterProxyModel):
    '''
    Supports filtering and sorting of images by tag.
    Note/hack: Uses "FilterRegExp" as a comma-separated list of tags.
    '''

    def __init__(self, parent=None):
        QSortFilterProxyModel.__init__(self, parent)
        self.filter_tags = []
        self.filter_url = ""
        self.setDynamicSortFilter(True)

    def lessThan(self, left_qmi, right_qmi):
        '''
        If data at left_qmi matches fewer tags than data at right_qmi returns
        True. Returns False otherwise.
        '''
        left_tags = self.sourceModel().data(left_qmi, ImageModel.TagRole)
        left_int = set(self.filter_tags).intersection(set(left_tags))

        right_tags = self.sourceModel().data(right_qmi, ImageModel.TagRole)
        right_int = set(self.filter_tags).intersection(set(right_tags))

        return len(left_int) < len(right_int)

    def setFilterTags(self, tags):
        '''
        Filters on tags (a list)
        '''
        tags = [t for t in tags if t]
        self.filter_tags = tags
        self.setFilterRegExp("") # hack: triggers filter logic

    def setFilterUrl(self, url):
        '''
        Filters on url
        '''
        self.filter_url = url
        self.setFilterRegExp("") # hack: triggers filter logic

    def setFilterTagsString(self, string):
        '''
        Filters on tags (a string containing a space-separated list of tags).
        '''
        self.setFilterTags(string.split(" "))

    def filterAcceptsRow(self, row_index, parent_qmi):
        '''
        If data at row_index contains *ANY* tags in self.filterRegEx() returns
        True. Returns False otherwise.
        '''

        qmi = self.sourceModel().index(row_index, 0, parent_qmi)
        tags = self.sourceModel().data(qmi, ImageModel.TagRole)
        url = self.sourceModel().data(qmi, ImageModel.UrlRole)

        # if no tags set, show all images
        if self.filter_tags:
            intersection  = set(tags).intersection(set(self.filter_tags))
        else:
            intersection = True

        return bool(intersection) and self.filter_url in url

    def filterAcceptsColumn(*args, **kwargs):
        '''
        Model and view only have one column, so always return true.
        '''
        return True

    def deleteImage(self, qmi):
        url = self.data(qmi, ImageModel.UrlRole)
        self.beginRemoveRows(qmi, qmi.row(), qmi.row())
        self.sourceModel().deleteImage(url)
        self.endRemoveRows()

    def getLocalFilepath(self, url):
        '''
        Gets local file path to store image at URL at.
        '''
        return self.sourceModel().image_path(url)

    def addImage(self, url, local_path):
        '''
        Adds image at (absolute) local_path to model.
        '''
        return self.sourceModel().addImage(url, [], local_path)

