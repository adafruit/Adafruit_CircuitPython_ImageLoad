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
`adafruit_imageload.tests.test_palette_c_interface`
====================================================

These tests are to validate the displayio_shared_bindings classes that other tests are built on.

* Author(s):  Matt Land

"""
from unittest import TestCase
from .displayio_shared_bindings import Palette_C_Interface


class TestPalette_C_Interface(TestCase):
    def test_init_mono(self):
        Palette_C_Interface(1)

    def test_init_color(self):
        Palette_C_Interface(256)

    def test_set_int(self):
        palette = Palette_C_Interface(1)
        palette[0] = 0xFFFFFF

    def test_get_int(self):
        palette = Palette_C_Interface(1)
        palette[0] = 0xFFFFFF
        self.assertEqual(0xFFFFFF, palette[0])

    def test_set_byte(self):
        palette = Palette_C_Interface(1)
        palette[0] = b"\xFF\xFF\xFF"

    def test_get_byte(self):
        palette = Palette_C_Interface(1)
        palette[0] = b"\xFF\xFF\xFF"
        self.assertEqual(b"\xFF\xFF\xFF", palette[0])

    def test_set_bytearray(self):
        palette = Palette_C_Interface(1)
        palette[0] = bytearray(b"\xFF\xFF\xFF")

    def test_prevents_out_of_range(self):
        palette = Palette_C_Interface(1)
        try:
            palette[1] = 0xFFFFFF
            self.fail("exception should have already thrown")
        except ValueError as e:
            if "greater than allowed" not in str(e):
                raise

    def test_prevents_set_non_allowed(self):
        palette = Palette_C_Interface(1)
        try:
            palette[0] = "\xFF\xFF\xFF"  # attempt with a string, which is not allowed
            self.fail("exception should have thrown")
        except ValueError as e:
            if "should be" not in str(e):
                raise

    def test_validate_success(self):
        palette = Palette_C_Interface(1)
        palette[0] = b"\xFF\xFF\xFF"
        palette.validate()

    def test_validate_fails(self):
        palette = Palette_C_Interface(2)
        palette[1] = b"\xFF\xFF\xFF"
        try:
            palette.validate()
            self.fail("exception should have thrown")
        except IndexError as e:
            if "palette was initialized" not in str(e):
                raise

    def test_str(self):
        palette = Palette_C_Interface(1)
        palette[0] = b"\xFF\xFF\xFF"
        print(str(palette))
