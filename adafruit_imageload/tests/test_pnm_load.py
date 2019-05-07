from unittest import TestCase
from adafruit_imageload import pnm
from io import BytesIO
import logging
import os

class Bitmap(object):
    def __init__(self, width, height, colors):
        self.width = width
        self.height = height
        self.colors = colors

logging.getLogger().setLevel(logging.INFO)

class TestPnmLoad(TestCase):

    def test_load_fails_with_no_header_data(self):
        f = BytesIO(b"some initial binary data: \x00\x01")
        try:
            pnm.load(f, b'P1', bitmap=Bitmap)
            self.fail('should have failed')
        except Exception as e:
            if "Unsupported image format" not in str(e):
                raise

    def test_load_works_p1_ascii(self):
        test_file = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'images', 'netpbm_p1_mono.pbm')
        with open(test_file, 'rb') as f:
            bitmap, palette = pnm.load(f, b'P1', bitmap=Bitmap)
        self.assertTrue(isinstance(bitmap, Bitmap), bitmap)
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(13, bitmap.width)
        self.assertEqual(21, bitmap.height)

    def test_load_works_p4_binary(self):
        test_file = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'images', 'netpbm_p4_mono.pbm')
        with open(test_file, 'rb') as f:
            bitmap, palette = pnm.load(f, b'P4', bitmap=Bitmap)
        self.assertTrue(isinstance(bitmap, Bitmap))
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(8, bitmap.width)
        self.assertEqual(8, bitmap.height)

    def test_load_works_p4_binary_high_res(self):
        test_file = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'images', 'MARBLES.PBM')
        with open(test_file, 'rb') as f:
            bitmap, palette = pnm.load(f, b'P4', bitmap=Bitmap)
        self.assertTrue(isinstance(bitmap, Bitmap))
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(1152, bitmap.width)
        self.assertEqual(813, bitmap.height)