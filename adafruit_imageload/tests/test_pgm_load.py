import os
from unittest import TestCase
from adafruit_imageload import pnm
from .displayio_shared_bindings import Bitmap_C_Interface, Palette_C_Interface


class TestPgmLoad(TestCase):
    def test_load_works_p2_ascii(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "examples",
            "images",
            "netpbm_p2_ascii.pgm",
        )
        with open(test_file, "rb") as f:
            bitmap, palette = pnm.load(
                f, b"P2", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
            )
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)
        self.assertEqual(6, bitmap.colors)
        self.assertEqual(8, bitmap.width)
        self.assertEqual(8, bitmap.height)
        bitmap.validate()
        self.assertEqual(6, palette.num_colors)
        palette.validate()
        # self.fail(str(palette))

    def test_load_works_p5_binary(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "examples",
            "images",
            "netpbm_p5_binary.pgm",
        )
        with open(test_file, "rb") as f:
            bitmap, palette = pnm.load(
                f, b"P5", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
            )
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)

        self.assertEqual(8, palette.num_colors)
        palette.validate()
        self.assertEqual(8, bitmap.colors)
        self.assertEqual(8, bitmap.width)
        self.assertEqual(8, bitmap.height)
        bitmap.validate()
        # self.fail(str(bitmap))
