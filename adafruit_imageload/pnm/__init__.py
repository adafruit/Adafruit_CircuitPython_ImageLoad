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
`adafruit_imageload.pnm`
====================================================

Load pixel values (indices or colors) into a bitmap and colors into a palette.

* Author(s): Matt Land, Brooke Storm, Sam McGahan

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad.git"


def load(file, header, *, bitmap=None, palette=None):
    # Read the header
    magic_number = header[:2]
    file.seek(2)
    pnm_header = []
    while True:
        # We have all we need at length 3
        if len(pnm_header) == 3:
            break
        if len(pnm_header) == 2 and (
            magic_number.startswith(b"P1") or magic_number.startswith(b"P4")
        ):
            bitmap = bitmap(pnm_header[0], pnm_header[1], 1)
            if palette:
                palette = palette(1)
                palette[0] = 0xFFFFFF
            if magic_number.startswith(b"P1"):
                from . import pbm_ascii

                return pbm_ascii.load(
                    file, pnm_header[0], pnm_header[1], bitmap=bitmap, palette=palette
                )

            from . import pbm_binary

            return pbm_binary.load(
                file, pnm_header[0], pnm_header[1], bitmap=bitmap, palette=palette
            )

        next_byte = file.read(1)
        if next_byte == b"#":
            while True:
                next_byte = file.read(1)
                if not next_byte:
                    raise RuntimeError("Unsupported image format")
                if next_byte == b"\n":
                    break
        if next_byte.isdigit():
            value = bytearray()
            while True:
                if not next_byte.isdigit():
                    break
                value += next_byte
                next_byte = file.read(1)
                if not next_byte:
                    raise RuntimeError("Unsupported image format")

            pnm_header.append(int("".join(["%c" % char for char in value])))
            continue

        if not next_byte:
            raise RuntimeError("Unsupported image format")

    if magic_number.startswith(b"P2") or magic_number.startswith(b"P5"):
        from . import pgm

        return pgm.load(file, magic_number, pnm_header, bitmap=bitmap, palette=palette)

    if magic_number.startswith(b"P3") or magic_number.startswith(b"P6"):
        from . import ppm

        return ppm.load(file, magic_number, pnm_header, bitmap=bitmap, palette=palette)

    raise RuntimeError("Unsupported image format")
