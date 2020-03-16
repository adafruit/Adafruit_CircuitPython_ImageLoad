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
`adafruit_imageload.pnm.pgm`
====================================================

Load pixel values (indices or colors) into a bitmap and colors into a palette.

* Author(s): Matt Land, Brooke Storm, Sam McGahan

"""
# pylint: disable=import-outside-toplevel


def load(file, magic_number, header, *, bitmap=None, palette=None):
    """
    Perform the load of Netpbm greyscale images (P2, P5)
    """
    if header[2] > 256:
        raise NotImplementedError("16 bit files are not supported")
    width = header[0]
    height = header[1]

    if magic_number == b"P2":  # To handle ascii PGM files.
        from . import ascii as pgm_ascii

        return pgm_ascii.load(file, width, height, bitmap=bitmap, palette=palette)

    if magic_number == b"P5":  # To handle binary PGM files.
        from . import binary

        return binary.load(file, width, height, bitmap=bitmap, palette=palette)

    raise NotImplementedError("Was not able to send image")
