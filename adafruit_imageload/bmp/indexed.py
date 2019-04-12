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
`adafruit_imageload.bmp.indexed`
====================================================

Load pixel values (indices or colors) into a bitmap and colors into a palette from an indexed BMP.

* Author(s): Scott Shawcroft

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad.git"

import math

def load(f, width, height, data_start, colors, color_depth, *, bitmap=None, palette=None):
    if palette:
        palette = palette(colors)

        f.seek(data_start - colors * 4)
        for color in range(colors):
            c = f.read(4)
            palette[color] = c

    if bitmap:
        minimum_color_depth = 1
        while colors > 2 ** minimum_color_depth:
            minimum_color_depth *= 2

        bitmap = bitmap(width, height, colors)
        f.seek(data_start)
        line_size = width // (8 // color_depth)
        if line_size % 4 != 0:
            line_size += (4 - line_size % 4)

        chunk = bytearray(line_size)

        for y in range(height-1,-1,-1):
            f.readinto(chunk)
            pixels_per_byte = 8 // color_depth
            offset = y * width

            for x in range(width):
                ci = x // pixels_per_byte
                pixel = (chunk[ci] >> (8 - color_depth*(x % pixels_per_byte + 1))) & ((1 << minimum_color_depth) - 1)
                bitmap[offset + x] = pixel

    return bitmap, palette
