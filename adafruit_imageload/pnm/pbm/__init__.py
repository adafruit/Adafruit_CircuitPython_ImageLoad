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
`adafruit_imageload.pnm.pbm`
====================================================

Load pixel values (indices or colors) into a bitmap and for a binary ppm,
return None for pallet.

* Author(s):  Matt Land, Brooke Storm, Sam McGahan

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad.git"


def load(f, magic_number, header, bitmap=None, palette=None):
    """
    Load a P1 or P4 Netpbm 'PBM' image into the displayio.Bitmap
    """
    width = header[0]
    height = header[1]

    if palette:
        palette = palette(1)
    if bitmap:
        bitmap = bitmap(width, height, 1)
        if magic_number == b'P1':  # ASCII space packed file
            next_byte = True
            for y in range(height):
                x = 0
                while next_byte:
                    next_byte = f.read(1)
                    if not next_byte.isdigit():
                        continue
                    bitmap[x, y] = 1 if next_byte == b'1' else 0
                    if x == width - 1:
                        break
                    x += 1
            return bitmap, palette
        if magic_number == b'P4':  # binary read from file as hex
            x = 0
            y = 0
            while True:
                next_byte = f.read(1)
                if not next_byte:
                    break  # out of bits
                for bit in iterbits(int.from_bytes(next_byte, byteorder='little')):
                    bitmap[x, y] = bit
                    x += 1
                    if x > width - 1:
                        y += 1
                        x = 0
                    if y > height - 1:
                        break
            return bitmap, palette
        raise NotImplementedError('magic number {}'.format(magic_number))


def iterbits(b):
    for i in range(8):
        yield (b >> i) & 1
