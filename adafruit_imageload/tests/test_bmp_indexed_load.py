import os
from unittest import TestCase
from adafruit_imageload import load
from .displayio_shared_bindings import Bitmap_C_Interface, Palette_C_Interface


class TestBmpIndexedLoad(TestCase):
    def test_load_works_p1_ascii(self):
        test_file = os.path.join(
            os.path.dirname(__file__), "..", "..", "examples", "images", "4bit.bmp"
        )

        bitmap, palette = load(
            filename=test_file, bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
        )
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)
        self.assertEqual(16, bitmap.colors)
        self.assertEqual(15, bitmap.width)
        self.assertEqual(17, bitmap.height)

        bitmap.validate()
        # uncomment line below to see a string representation of the object
        # self.fail(str(bitmap))
        self.assertEqual(5, bitmap[0])  # check first row
        self.assertEqual(5, bitmap[11, 1])  # check second row

        self.assertEqual(16, palette.num_colors)
        palette.validate()
        # uncomment line below to see a string representation of the object
        # self.fail(str(palette))
