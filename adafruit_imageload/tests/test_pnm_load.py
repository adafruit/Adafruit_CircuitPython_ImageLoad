from unittest import TestCase
from adafruit_imageload import pnm
from io import BytesIO
import logging
import os


class Bitmap_C_Interface(object):
    def __init__(self, width, height, colors):
        self.width = width
        self.height = height
        self.colors = colors
        self.data = {}

    def __setitem__(self, key, value):
        if key > self.height - 1:
            raise RuntimeError('illegal column')
        try:
            self.data[key]
        except KeyError:
            self.data[key] = bytearray()
        if len(self.data[key]) >= self.width:
            raise RuntimeError('row too wide')
        logging.info(value)
        self.data[key] += value

    def __getitem__(self, item: str) -> bytearray:
        try:
            return self.data[item]
        except KeyError:
            return bytearray()

    @property
    def data_height(self) -> int:
        return len(self.data)

    @property
    def data_width(self) -> int:
        return len(self.data[0])

    def validate(self):
        if not self.data:
            raise ValueError('no rows were set / no data in memory')
        for line in self.data:
            if len(self.data[line]) != self.width:
                raise ValueError(f'row {line} has {self.data[line]} bits, should have {self.width}')

    def __str__(self):
        out = '\n'
        for line in self.data:
            out += f'{self.data[line]}\n'
        return out

logging.getLogger().setLevel(logging.INFO)

class TestPnmLoad(TestCase):

    def test_load_fails_with_no_header_data(self):
        f = BytesIO(b"some initial binary data: \x00\x01")
        try:
            pnm.load(f, b'P1', bitmap=Bitmap_C_Interface)
            self.fail('should have failed')
        except Exception as e:
            if "Unsupported image format" not in str(e):
                raise

    def test_load_works_p1_ascii(self):
        test_file = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'images', 'netpbm_p1_mono.pbm')
        with open(test_file, 'rb') as f:
            bitmap, palette = pnm.load(f, b'P1', bitmap=Bitmap_C_Interface)
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(13, bitmap.width)
        self.assertEqual(21, bitmap.height)

        bitmap.validate()
        self.assertEqual(bytearray(b'0000000000000'), bitmap[0])  # check first row
        self.assertEqual(bytearray(b'0000010000010'), bitmap[1])  # check second row

    def test_load_works_p4_in_mem(self):
        f = BytesIO(b"P4\n 4 2\n\x00\x00\x00\x00\x00\x00\x00\x00")
        bitmap, palette = pnm.load(f, b'P4', bitmap=Bitmap_C_Interface)
        self.assertEqual(4, bitmap.width)
        self.assertEqual(4, bitmap.height)
        bitmap.validate()

    def test_load_works_p4_binary(self):
        test_file = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'images', 'netpbm_p4_mono.pbm')
        with open(test_file, 'rb') as f:
            bitmap, palette = pnm.load(f, b'P4', bitmap=Bitmap_C_Interface)
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface))
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(8, bitmap.width)
        self.assertEqual(8, bitmap.height)
        bitmap.validate()

    def test_load_works_p4_binary_high_res(self):
        test_file = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'images', 'netpbm_p4_mono_large.pbm')
        with open(test_file, 'rb') as f:
            bitmap, palette = pnm.load(f, b'P4', bitmap=Bitmap_C_Interface)
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface))
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(1152, bitmap.width)
        self.assertEqual(813, bitmap.height)


class TestPPMLoad(TestCase):

    def test_load_works_p1_ascii(self):
        test_file = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'images', 'netpbm_p3_rgb_ascii.ppm')
        with open(test_file, 'rb') as f:
            bitmap, palette = pnm.load(f, b'P3', bitmap=Bitmap_C_Interface)
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)
        self.assertEqual(16777216, bitmap.colors)
        self.assertEqual(16, bitmap.width)
        self.assertEqual(16, bitmap.height)
        bitmap.validate()
        self.fail(bitmap.data)
        self.fail(str(bitmap))
