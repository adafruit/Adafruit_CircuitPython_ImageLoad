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
`adafruit_imageload.tests.test_pbm_load`
====================================================

* Author(s):  Matt Land

"""
import os
from io import BytesIO
from unittest import TestCase
from adafruit_imageload import pnm
from adafruit_imageload.pnm.pbm_binary import iterbits, reverse
from .displayio_shared_bindings import Bitmap_C_Interface, Palette_C_Interface


class TestPbmLoad(TestCase):
    def test_load_fails_with_no_header_data(self):
        file = BytesIO(b"some initial binary data: \x00\x01")
        try:
            pnm.load(
                file, b"P1", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
            )
            self.fail("should have failed")
        except Exception as caught_exception:
            if "Unsupported image format" not in str(caught_exception):
                raise

    def test_load_works_p1_ascii(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "images",
            "netpbm_p1_mono_ascii.pbm",
        )
        with open(test_file, "rb") as file:
            bitmap, palette = pnm.load(
                file, b"P1", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
            )
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(13, bitmap.width)
        self.assertEqual(21, bitmap.height)

        bitmap.validate()
        self.assertEqual(0, bitmap[0])  # check first row
        self.assertEqual(1, bitmap[11, 1])  # check second row

        self.assertEqual(1, palette.num_colors)
        palette.validate()

    def test_load_works_p4_in_mem(self):
        file = BytesIO(b"P4\n4 2\n\x55")
        bitmap, palette = pnm.load(
            file, b"P4", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
        )
        self.assertEqual(4, bitmap.width)
        self.assertEqual(2, bitmap.height)
        bitmap.validate()
        self.assertEqual("\n   0   1   0   1\n   0   1   0   1\n", str(bitmap))
        palette.validate()

    def test_load_works_p4_binary(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "images",
            "netpbm_p4_mono_binary.pbm",
        )
        with open(test_file, "rb") as file:
            bitmap, palette = pnm.load(
                file, b"P4", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
            )
        self.assertEqual(1, palette.num_colors)
        palette.validate()
        self.assertEqual(b"\xff\xff\xff", palette[0])
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface))
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(32, bitmap.width)
        self.assertEqual(15, bitmap.height)
        bitmap.validate()

    def test_load_works_p4_binary_high_res(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "images",
            "netpbm_p4_mono_large.pbm",
        )
        with open(test_file, "rb") as file:
            bitmap, palette = pnm.load(
                file, b"P4", bitmap=Bitmap_C_Interface, palette=Palette_C_Interface
            )
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface))
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(320, bitmap.width)
        self.assertEqual(240, bitmap.height)
        bitmap.validate()
        self.assertEqual(1, palette.num_colors)
        palette.validate()

    def test_iterbits(self):
        k = b"k"
        bits = []
        for byte in iterbits(k):
            bits.append(byte)
        # self.assertEqual([0,1,1,0,1,0,1,1], bits[::-1])
        self.assertEqual([0, 1, 1, 0, 1, 0, 1, 1], bits)

    def test_reverse(self):
        # 00110100 to 00101100
        self.assertEqual(reverse(0x34), 0x2C)
        self.assertEqual(reverse(0xFF), 0xFF)
        self.assertEqual(reverse(0x00), 0x00)
        self.assertEqual(reverse(0x0E), 0x70)
