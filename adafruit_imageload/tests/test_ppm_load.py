import os
import logging
from unittest import TestCase
from adafruit_imageload import pnm
from .displayio_shared_bindings import Bitmap_C_Interface, Palette_C_Interface

logging.getLogger().setLevel(logging.INFO)


class TestPpmLoad(TestCase):
    def test_load_works_p3_ascii(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "examples",
            "images",
            "netpbm_p3_rgb_ascii.ppm",
        )
        with open(test_file, "rb") as file:
            bitmap, palette = pnm.load(
                file, b"P3", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
            )

        self.assertTrue(isinstance(palette, Palette_C_Interface))
        self.assertEqual(6, palette.num_colors)
        #self.fail(str(palette))
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)
        self.assertEqual(6, bitmap.colors)
        self.assertEqual(16, bitmap.width)
        self.assertEqual(16, bitmap.height)
        bitmap.validate()
        palette.validate()

    def test_load_works_p6_binary(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "examples",
            "images",
            "netpbm_p6_binary.ppm",
        )
        with open(test_file, "rb") as f:
            bitmap, palette = pnm.load(
                f, b"P6", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
            )
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)
        self.assertEqual(6, bitmap.colors)
        self.assertEqual(16, bitmap.width)
        self.assertEqual(16, bitmap.height)
        bitmap.validate()
        str(bitmap)
        palette.validate()
