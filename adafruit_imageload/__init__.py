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
`adafruit_imageload`
====================================================

Load pixel values (indices or colors) into a bitmap and colors into a palette.

* Author(s): Scott Shawcroft

"""
# pylint: disable=import-outside-toplevel

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad.git"


def load(filename, *, bitmap=None, palette=None):
    """Load pixel values (indices or colors) into a bitmap and colors into a palette.

       bitmap is the desired type. It must take width, height and color_depth in the constructor. It
       must also have a _load_row method to load a row's worth of pixel data.

       palette is the desired pallete type. The constructor should take the number of colors and
       support assignment to indices via [].
    """
    if not bitmap or not palette:
        try:
            # use displayio if available
            import displayio

            if not bitmap:
                bitmap = displayio.Bitmap
            if not palette:
                palette = displayio.Palette
        except ModuleNotFoundError:
            # meh, we tried
            pass

    with open(filename, "rb") as file:
        header = file.read(3)
        file.seek(0)
        if header.startswith(b"BM"):
            from . import bmp

            return bmp.load(file, bitmap=bitmap, palette=palette)
        if header.startswith(b"P"):
            from . import pnm

            return pnm.load(file, header, bitmap=bitmap, palette=palette)
        if header.startswith(b"GIF"):
            from . import gif

            return gif.load(file, bitmap=bitmap, palette=palette)
        raise RuntimeError("Unsupported image format")
