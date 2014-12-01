from unittest import TestCase
from trollbox.image_model import ImageModel
from PySide.QtGui import QApplication
from PySide.QtCore import Qt

import json, tempfile, os, subprocess

app = None

class Test_ImageModel(TestCase):
    def setUp(self):
        global app
        if not app:
            app = QApplication([])

    def test_instantiation(self):
        temp_dir = tempfile.mkdtemp()
        model = ImageModel(troll_dir=temp_dir)
        self.assertEqual(model.rowCount(), 0)
        subprocess.call(["rm", "-rf", temp_dir]) 

    def test_load(self):
        file_dir = os.path.dirname(os.path.realpath(__file__))
        sample_path = os.path.join(file_dir, "data", "0")
        model = ImageModel(troll_dir=sample_path)

        index = model.index(0, 0)
        self.assertEqual(model.data(index, Qt.DisplayRole), "http://foo.bar")
        self.assertEqual(model.data(index, ImageModel.TagRole), ["tng", "book"])

        index = model.index(1, 0)
        self.assertEqual(model.data(index, ImageModel.TagRole), ["koop", "postmaster"])

    def test_addImage(self):

        # create a troll box in a temp dir and add an image from the "0" test 
        # data set
        file_dir = os.path.dirname(os.path.realpath(__file__))
        sample_path = os.path.join(file_dir, "data", "0", "images", "book.jpg")
        temp_dir = tempfile.mkdtemp()
        try:
            model = ImageModel(troll_dir=temp_dir)
            model.addImage("http://foo.bar", ["tng"], sample_path)

            index = model.index(0, 0)
            self.assertEqual(model.data(index, Qt.DisplayRole), "http://foo.bar")
        finally:
            subprocess.call(["rm", "-rf", temp_dir])

    def test_save(self):

        # create a troll box in a temp dir and add an image from the "0" test 
        # data set, save it, and verify another model picks up the changes
        file_dir = os.path.dirname(os.path.realpath(__file__))
        sample_path = os.path.join(file_dir, "data", "0", "images", "book.jpg")
        temp_dir = tempfile.mkdtemp()
        try:
            model = ImageModel(troll_dir=temp_dir)
            model.addImage("http://foo.bar", ["tng"], sample_path)

            model_b = ImageModel(troll_dir=temp_dir)

            self.assertEqual(model_b.data(model.index(0, 0), Qt.DisplayRole), "http://foo.bar")
        finally:
            subprocess.call(["rm", "-rf", temp_dir])

    def test_setData(self):

        # create a troll box in a temp dir, add an image from the "0" test 
        # data set, and modify it via setData
        file_dir = os.path.dirname(os.path.realpath(__file__))
        sample_path = os.path.join(file_dir, "data", "0", "images", "book.jpg")
        temp_dir = tempfile.mkdtemp()
        try:
            model = ImageModel(troll_dir=temp_dir)
            model.addImage("http://foo.bar", ["tng"], sample_path)
            self.assertEqual(model.data(model.index(0, 0), Qt.DisplayRole), "http://foo.bar")
            
            model.setData(model.index(0, 0), "http://bar.bar", Qt.DisplayRole)
            self.assertEqual(model.data(model.index(0, 0), Qt.DisplayRole), "http://bar.bar")

            sample_path = os.path.join(file_dir, "data", "0", "images", "koop.jpg")
            model.setData(model.index(0, 0), sample_path, Qt.DecorationRole)
            # no good way to check icon currently
        finally:
            subprocess.call(["rm", "-rf", temp_dir])


