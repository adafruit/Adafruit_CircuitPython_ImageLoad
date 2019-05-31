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
`adafruit_imageload.tests.test_bmp_indexed_load`
====================================================

* Author(s):  Matt Land

"""

import os
from unittest import TestCase
from adafruit_imageload import load
from .displayio_shared_bindings import Bitmap_C_Interface, Palette_C_Interface


class TestBmpIndexedLoad(TestCase):
    def test_order_bgra_to_rgba(self):
        test_file = os.path.join(
            os.path.dirname(__file__), "..", "examples", "images", "4bit.bmp"
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
        # make sure bye order swapped
        self.assertTrue(palette[4] in [b"\x9d\x00\xff\x00", b"\x9d\x00\xff"])
        # uncomment line below to see a string representation of the object
        # self.fail(str(palette))
