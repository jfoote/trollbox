from PySide.QtGui import *
from PySide.QtCore import QSize, Qt, Signal, Slot, QModelIndex
from trollbox.image_model import ImageModel
from trollbox.image_searcher import ImageSearcher

class ImagePicker(QListView):
    '''
    QListView widget used to represent the local image collection. Designed
    to use a ImageSearcher as a QSortFilterProxyModel and an ImageModel as
    the underlying model.
    '''

    # Signals
    selectedTagsStringChanged = Signal(str)
    selectedUrlChanged = Signal(str)
    preDelete = Signal()

    def __init__(self, parent=None, model_path=None):
        QListView.__init__(self, parent)

        self.setViewMode(QListView.IconMode)
        self.setDragEnabled(False)
        self.setAcceptDrops(False)
        self.setIconSize(QSize(150,150))
        self.setSelectionMode(self.SingleSelection)

        imageModel = ImageModel(parent, model_path)
        proxyModel = ImageSearcher(parent)
        proxyModel.setSourceModel(imageModel)
        self.setModel(proxyModel)

        imageModel.imageAdded.connect(self.handleImageAdded)
        imageModel.rowsAboutToBeRemoved.connect(self.handlePreDelete)

    def handleImageAdded(self, modelRow):
        '''
        Clears the current search and selects the new image
        '''
        self.setFilterTagsString("")
        print "rowCount()", self.model().rowCount()
        qmi = self.model().index(self.model().rowCount()-1, 0)
        print "handleImageAdded", qmi
        self.selectionModel().select(qmi, self.selectionModel().ClearAndSelect)
        self.scrollTo(qmi)

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
        '''

        indexes = cur_sel.indexes() 
        if not indexes: # no selection
            print "no selection"
            tags = ""
            url = ""
        else:
            cur_qmi = cur_sel.indexes()[0] # only allow 1 item at a time
            tags = self.model().data(cur_qmi, ImageModel.TagRole)
            url = self.model().data(cur_qmi, ImageModel.UrlRole)

        self.selectedTagsStringChanged.emit(" ".join(tags))
        self.selectedUrlChanged.emit(url)
        print "emitted selectionChanged:", url, tags

    def deleteSelected(self):
        indexes = self.selectedIndexes() 
        if not indexes: # no selection
            return
        cur_qmi = indexes[0] # only allow 1 item at a time
        print "deleting", self.model().data(cur_qmi, ImageModel.UrlRole)
        row = cur_qmi.row()
        self.model().deleteImage(cur_qmi) # calls proxy model
        print "deleted"

    def handlePreDelete(self, qmi, first, last):
        self.preDelete.emit()

    @Slot(QModelIndex, QModelIndex)
    def currentChanged(self, cur_qmi, prev_qmi):
        '''
        Does default stuff + emits signals
        NOTE: Called *before* selection is changed
        '''
        QListView.currentChanged(self, cur_qmi, prev_qmi)
        '''

        tags = self.model().data(cur_qmi, ImageModel.TagRole)
        print "emitting"
        self.selectedTagsStringChanged.emit(" ".join(tags))

        url = self.model().data(cur_qmi, ImageModel.UrlRole)
        self.selectedUrlChanged.emit(url)
        '''

    @Slot(str)
    def setTagsString(self, string):
        tags = string.split(" ")
        indexes = self.selectedIndexes()
        if not indexes:
            return # no selection
        qmi = indexes[0] # only allow 1 selection at a time
        print "qmi", qmi, "tags", tags
        self.model().setData(qmi, tags, ImageModel.TagRole)

    def setFilterTags(self, *args, **kwargs):
        self.model().setFilterTags(*args, **kwargs)

    def setFilterTagsString(self, *args, **kwargs):
        self.model().setFilterTagsString(*args, **kwargs)

    def setFilterUrl(self, *args, **kwargs):
        self.model().setFilterUrl(*args, **kwargs)

    def sort(self, col=0, order=Qt.DescendingOrder):
        '''
        Sorts in descending order (Qt default is Ascending)
        '''
        self.model().sort(col, order)

    def getLocalFilepath(self, url):
        '''
        Gets local file path to store image at URL at.
        '''
        return self.model().getLocalFilepath(url)

    def addImage(self, url, local_path):
        '''
        Adds image at (absolute) local_path to model.
        '''
        return self.model().addImage(url, local_path)
