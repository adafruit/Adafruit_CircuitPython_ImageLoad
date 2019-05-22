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
`adafruit_imageload.pnm.pgm.ascii`
====================================================

Load pixel values (indices or colors) into a bitmap and colors into a palette.

* Author(s): Matt Land, Brooke Storm, Sam McGahan

"""


def load(file, width, height, bitmap=None, palette=None):
    """
    Load a PGM ascii file (P2)
    """
    data_start = file.tell()  # keep this so we can rewind
    palette_colors = set()
    pixel = bytearray()
    # build a set of all colors present in the file, so palette and bitmap can be constructed
    while True:
        byte = file.read(1)
        if byte == b"":
            break
        if not byte.isdigit():
            int_pixel = int("".join(["%c" % char for char in pixel]))
            palette_colors.add(int_pixel)
            pixel = bytearray()
        pixel += byte
    if palette:
        palette = build_palette(palette, palette_colors)
    if bitmap:
        bitmap = bitmap(width, height, len(palette_colors))
        palette_colors = list(palette_colors)
        file.seek(data_start)
        for y in range(height):
            for x in range(width):
                pixel = bytearray()
                while True:
                    byte = file.read(1)
                    if not byte.isdigit():
                        break
                    pixel += byte
                int_pixel = int("".join(["%c" % char for char in pixel]))
                bitmap[x, y] = palette_colors.index(int_pixel)
    return bitmap, palette


def build_palette(palette_class, palette_colors):
    """
    construct the Palette, and populate it with the set of palette_colors
    """
    palette = palette_class(len(palette_colors))
    for counter, color in enumerate(palette_colors):
        palette[counter] = bytes([color, color, color])
    return palette
