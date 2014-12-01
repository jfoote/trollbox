from unittest import TestCase
from trollbox.image_picker import ImagePicker, ImageSearcher
from PySide.QtGui import QApplication
from PySide.QtCore import Qt

import json, tempfile, os, subprocess

app = None

class Test_ImageSearcher(TestCase):
    def setUp(self):
        global app
        if not app:
            #app = QApplication([])
            pass

    def test_instantiation(self):
        i = ImageSearcher()
        i = ImagePicker()

    def test_filter(self):
        file_dir = os.path.dirname(os.path.realpath(__file__))
        sample_path = os.path.join(file_dir, "data", "0")
        ip = ImagePicker(model_path=sample_path)

        # hacky, but: set a filter that should only match one image in the 
        # test set and verify only one image exists afterward
        ip.setFilterTags(["hardway"])
        self.assertEqual(ip.model().rowCount(), 1)
