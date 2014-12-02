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

    # Signals
    tagsStringChanged = Signal(str)
    urlChanged = Signal(str)

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

    @Slot(QItemSelection, QItemSelection)
    def selectionChanged(self, cur_sel, prev_sel):
        '''
        NOTE: Called *after* selection is made
        '''
        QListView.selectionChanged(self, cur_sel, prev_sel)
        '''
        It seems like using currentChanged to emit signals
        probably catches more corner cases, but this is left
        here for reference in case upstream slots need the
        selection to be set

        cur_qmi = cur_sel.indexes()[0] # only allow 1 item at a time

        tags = self.model().data(cur_qmi, ImageModel.TagRole)
        self.tagsStringChanged.emit(" ".join(tags))

        url = self.model().data(cur_qmi, Qt.DisplayRole)
        self.urlChanged.emit(url)

        print "index", self.selectedIndexes()
        '''

    @Slot(QModelIndex, QModelIndex)
    def currentChanged(self, cur_qmi, prev_qmi):
        '''
        Does default stuff + emits signals
        NOTE: Called *before* selection is changed
        '''
        QListView.currentChanged(self, cur_qmi, prev_qmi)

        tags = self.model().data(cur_qmi, ImageModel.TagRole)
        self.tagsStringChanged.emit(" ".join(tags))

        url = self.model().data(cur_qmi, Qt.DisplayRole)
        self.urlChanged.emit(url)

    @Slot(str)
    def setTagsString(self, string):
        tags = string.split(" ")
        indexes = self.selectedIndexes()
        if not indexes:
            return # no selection
        qmi = indexes[0] # only allow 1 selection at a time
        print "qmi", qmi, "tags", tags
        #self.model().setData(qmi, tags, ImageModel.TagRole)


    def setFilterTags(self, *args, **kwargs):
        self.model().setFilterTags(*args, **kwargs)

    def setFilterTagsString(self, *args, **kwargs):
        self.model().setFilterTagsString(*args, **kwargs)

    def sort(self, col=0, order=Qt.DescendingOrder):
        '''
        Sorts in descending order (Qt default is Ascending)
        '''
        self.model().sort(col, order)
