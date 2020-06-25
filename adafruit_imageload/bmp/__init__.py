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
`adafruit_imageload.bmp`
====================================================

Load pixel values (indices or colors) into a bitmap and colors into a palette from a BMP file.

* Author(s): Scott Shawcroft

"""
# pylint: disable=import-outside-toplevel

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad.git"


def load(file, *, bitmap=None, palette=None):
    """Loads a bmp image from the open ``file``.

       Returns tuple of bitmap object and palette object.

       :param object bitmap: Type to store bitmap data. Must have API similar to `displayio.Bitmap`.
         Will be skipped if None
       :param object palette: Type to store the palette. Must have API similar to
         `displayio.Palette`. Will be skipped if None"""
    file.seek(10)
    data_start = int.from_bytes(file.read(4), "little")
    # f.seek(14)
    # bmp_header_length = int.from_bytes(file.read(4), 'little')
    # print(bmp_header_length)
    file.seek(0x12)  # Width of the bitmap in pixels
    width = int.from_bytes(file.read(4), "little")
    try:
        height = int.from_bytes(file.read(4), "little")
    except OverflowError:
        raise NotImplementedError(
            "Negative height BMP files are not supported on builds without longint"
        )
    file.seek(0x1C)  # Number of bits per pixel
    color_depth = int.from_bytes(file.read(2), "little")
    file.seek(0x1E)  # Compression type
    compression = int.from_bytes(file.read(2), "little")
    file.seek(0x2E)  # Number of colors in the color palette
    colors = int.from_bytes(file.read(4), "little")

    if colors == 0 and color_depth >= 16:
        raise NotImplementedError("True color BMP unsupported")

    if compression > 2:
        raise NotImplementedError("bitmask compression unsupported")

    if colors == 0:
        colors = 2 ** color_depth
    from . import indexed

    return indexed.load(
        file,
        width,
        height,
        data_start,
        colors,
        color_depth,
        compression,
        bitmap=bitmap,
        palette=palette,
    )
