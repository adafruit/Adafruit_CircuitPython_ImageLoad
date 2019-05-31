# The MIT License (MIT)
#
# Copyright (c) 2019 Matt Land
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_imageload.tests.test_bgm_load`
====================================================

* Author(s):  Matt Land

"""
import os
from unittest import TestCase
from adafruit_imageload import pnm
from .displayio_shared_bindings import Bitmap_C_Interface, Palette_C_Interface


class TestPgmLoad(TestCase):
    def test_load_works_p2_ascii(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "images",
            "netpbm_p2_ascii.pgm",
        )
        with open(test_file, "rb") as file:
            bitmap, palette = pnm.load(
                file, b"P2", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
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
            "examples",
            "images",
            "netpbm_p5_binary.pgm",
        )
        with open(test_file, "rb") as file:
            bitmap, palette = pnm.load(
                file, b"P5", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
            )
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)

        self.assertEqual(8, palette.num_colors)
        palette.validate()
        self.assertEqual(8, bitmap.colors)
        self.assertEqual(8, bitmap.width)
        self.assertEqual(8, bitmap.height)
        bitmap.validate()
        # self.fail(str(bitmap))
