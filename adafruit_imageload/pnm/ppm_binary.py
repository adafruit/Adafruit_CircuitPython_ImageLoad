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
`adafruit_imageload.pnm.ppm_binary`
====================================================

Load pixel values (indices or colors) into a bitmap and for a binary ppm,
return None for pallet.

* Author(s):  Matt Land, Brooke Storm, Sam McGahan

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad.git"


def load(file, width, height, bitmap=None, palette=None):
    """Load pixel values (indices or colors) into a bitmap and for a binary
    ppm, return None for pallet."""

    data_start = file.tell()
    palette_colors = set()
    line_size = width * 3

    for y in range(height):
        data_line = iter(bytes(file.read(line_size)))
        for red in data_line:
            # red, green, blue
            palette_colors.add((red, next(data_line), next(data_line)))

    if palette:
        palette = palette(len(palette_colors))
        for counter, color in enumerate(palette_colors):
            palette[counter] = bytes(color)
    if bitmap:
        bitmap = bitmap(width, height, len(palette_colors))
        file.seek(data_start)
        palette_colors = list(palette_colors)
        for y in range(height):
            x = 0
            data_line = iter(bytes(file.read(line_size)))
            for red in data_line:
                # red, green, blue
                bitmap[x, y] = palette_colors.index(
                    (red, next(data_line), next(data_line))
                )
                x += 1

    return bitmap, palette
