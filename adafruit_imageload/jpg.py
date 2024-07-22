# SPDX-FileCopyrightText: 2024  Channing Ramos
#
# SPDX-License-Identifier: MIT

"""
`adafruit_imageload.jpg`
====================================================

Load a JPG into a bitmap by calling jpegio.

* Author(s): Channing Ramos

"""

#A separate try for jpegio. While it has wide support it is not universal, and this import may fail.
#If that happens an ImportError with a proper message needs to be raised
try:
    from jpegio import JpegDecoder
except ImportError:
    print("jpegio not supported on this board.")

try:
    from io import BufferedReader
    from typing import Tuple, Iterator, Optional, List
    from .displayio_types import PaletteConstructor, BitmapConstructor
except ImportError:
    pass

from displayio import Bitmap, ColorConverter, Colorspace

def load(file: BufferedReader,
         *,
         bitmap: BitmapConstructor,
         palette: Optional[PaletteConstructor] = None) -> Tuple[Bitmap, Optional[ColorConverter]]:

    decoder = JpegDecoder()
    width, height = decoder.open(file)
    bitmap_obj = bitmap(width, height, 65535)
    decoder.decode(bitmap_obj)

    return bitmap_obj, ColorConverter(input_colorspace=Colorspace.RGB565_SWAPPED)