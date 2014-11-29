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
        temp_dir = tempfile.mkdtemp()
        simple = {'foo' : 'bar'}
        json.dump(simple, open(os.path.join(temp_dir, "metadata.json"), "wt"))
        model = ImageModel(troll_dir=temp_dir)
        subprocess.call(["rm", "-rf", temp_dir])

    def test_addImage(self):
        temp_dir = tempfile.mkdtemp()
        model = ImageModel(troll_dir=temp_dir)
        file_dir = os.path.dirname(os.path.realpath(__file__))
        sample_path = os.path.join(file_dir, "data", "book.jpg")
        target_path = model.image_path("book.jpg")
        subprocess.call(["mkdir", "-p", model.image_dir()])
        subprocess.call(["cp", sample_path, target_path])
        model.addImage("http://foo.bar", ["tng"], target_path)
        subprocess.call(["rm", "-rf", temp_dir])

        self.assertEqual(model.data(0, Qt.DisplayRole), "http://foo.bar")

