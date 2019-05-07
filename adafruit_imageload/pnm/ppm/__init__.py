# The MIT License (MIT)
#
# Copyright (c) 2018 Scott Shawcroft for Adafruit Industries LLC
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
`adafruit_imageload.pnm.ppm`
====================================================

Load pixel values (indices or colors) into a bitmap and for a binary ppm,
return None for pallet.

* Author(s):  Matt Land, Brooke Storm, Sam McGahan

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad.git"

import math


def load(file, magic_number, header, bitmap=None, palette=None):
    """Load pixel values (indices or colors) into a bitmap and for a binary
    ppm, return None for pallet."""
    width = header[0]
    height = header[1]
    max_colors = (header[2] + 1) ** 3
    colors = math.log(header[2], 2)
    bitmap = bitmap(width, height, int(colors))
    palette = None

    if bitmap:
        if magic_number == b"P3":
            # This is ascii
            from . import ppm_ascii

            return ppm_ascii.load(
                file, width, height, max_colors, bitmap=bitmap, palette=None
            )

        minimum_color_depth = 1
        while max_colors > 2 ** minimum_color_depth:
            minimum_color_depth *= 2

        line_size = width * 3

        chunk = bytearray(line_size)

        for y in range(height):
            file.readinto(chunk)
            pixels_per_byte = 8 // max_colors
            offset = y * width

            for x in range(width):
                i = x // pixels_per_byte
                pixel = (
                    chunk[i] >> (8 - max_colors * (x % pixels_per_byte + 1))
                ) & ((1 << minimum_color_depth) - 1)
                bitmap[offset + x] = pixel

    return bitmap, palette
