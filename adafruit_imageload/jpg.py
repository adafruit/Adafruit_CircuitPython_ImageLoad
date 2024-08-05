# SPDX-FileCopyrightText: 2024  Channing Ramos
#
# SPDX-License-Identifier: MIT

"""
`adafruit_imageload.jpg`
====================================================

Load a JPG into a bitmap by calling the jpegio class.

* Author(s): Channing Ramos

"""

# A separate try for jpegio. Not every board supports it and this import may fail.
# If that happens an ImportError with a proper message needs to be raised
try:
    from jpegio import JpegDecoder
except ImportError:
    print("jpegio not supported on this board.")

try:
    from io import BufferedReader
    from typing import Optional, Tuple

    from .displayio_types import BitmapConstructor
except ImportError:
    pass

from displayio import Bitmap, ColorConverter, Colorspace

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad.git"


def load(
    file: BufferedReader,
    *,
    bitmap: BitmapConstructor,
) -> Tuple[Bitmap, Optional[ColorConverter]]:
    """
    Loads a JPG image from the open ''file''.
    The JPG must be a Baseline JPG, Progressive and Lossless JPG formats are not supported.

    Returns tuple of bitmap object and ColorConverter object.

    :param io.BufferedReader file: Open file handle or compatible (like 'io.BytesIO')
    :param object bitmap: Type to store bitmap data.
     Must have API similar to 'displayio.Bitmap'. Will be skipped if None.
     Will be skipped if None.
    """
    decoder = JpegDecoder()
    width, height = decoder.open(file)
    bitmap_obj = bitmap(width, height, 65535)
    decoder.decode(bitmap_obj)

    return bitmap_obj, ColorConverter(input_colorspace=Colorspace.RGB565_SWAPPED)
