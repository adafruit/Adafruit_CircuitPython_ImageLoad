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
`adafruit_imageload.tests.test_ppm_load`
====================================================

* Author(s):  Matt Land

"""
import os
from io import BytesIO
from unittest import TestCase
from adafruit_imageload import pnm
from adafruit_imageload.pnm.ppm_ascii import read_three_colors
from .displayio_shared_bindings import Bitmap_C_Interface, Palette_C_Interface


class TestPpmLoad(TestCase):
    def test_load_works_p3_ascii(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "images",
            "netpbm_p3_rgb_ascii.ppm",
        )
        with open(test_file, "rb") as file:
            bitmap, palette = pnm.load(
                file, b"P3", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
            )  # type: Bitmap_C_Interface, Palette_C_Interface

        self.assertTrue(isinstance(palette, Palette_C_Interface))
        self.assertEqual(6, palette.num_colors)
        palette.validate()
        # self.fail(str(palette))
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)
        self.assertEqual(6, bitmap.colors)
        self.assertEqual(16, bitmap.width)
        self.assertEqual(16, bitmap.height)
        bitmap.validate()

    def test_load_works_p6_binary(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "images",
            "netpbm_p6_binary.ppm",
        )
        with open(test_file, "rb") as file:
            bitmap, palette = pnm.load(
                file, b"P6", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
            )  # type: Bitmap_C_Interface, Palette_C_Interface
        self.assertEqual(6, palette.num_colors)
        palette.validate()
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)
        self.assertEqual(6, bitmap.colors)
        self.assertEqual(16, bitmap.width)
        self.assertEqual(16, bitmap.height)
        bitmap.validate()

    def test_load_three_colors_tail(self):
        buffer = BytesIO(b"211 222 233")
        for i in read_three_colors(buffer):
            self.assertEqual(b"\xd3\xde\xe9", i)

    def test_load_three_colors_middle(self):
        buffer = BytesIO(b"0 128 255 45 55 25")
        for i in iter(read_three_colors(buffer)):
            self.assertEqual(b"\x00\x80\xff", i)
            break
