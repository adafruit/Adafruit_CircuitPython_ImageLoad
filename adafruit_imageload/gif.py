# The MIT License (MIT)
#
# Copyright (c) 2019 Radomir Dopieralski
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
`adafruit_imageload.gif`
====================================================

Load pixel values (indices or colors) into a bitmap and colors into a palette
from a GIF file.

* Author(s): Radomir Dopieralski

"""

import struct


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad.git"

def load(file, *, bitmap=None, palette=None):
    """Loads a GIF image from the open ``file``.

       Returns tuple of bitmap object and palette object.

       :param object bitmap: Type to store bitmap data. Must have API similar to `displayio.Bitmap`.
         Will be skipped if None
       :param object palette: Type to store the palette. Must have API similar to
         `displayio.Palette`. Will be skipped if None"""
    header = file.read(6)
    if header not in {b'GIF87a', b'GIF89a'}:
        raise ValueError("Not a GIF file")
    w, h, flags, background, aspect = struct.unpack('<HHBBB', file.read(7))
    if (flags & 0x80) != 0:
        palette_size = 1 << ((flags & 0x07) + 1)
        palette_obj = palette(palette_size)
        for i in range(palette_size):
            palette_obj[i] = file.read(3)
    else:
        palette_obj = None
    color_bits = ((flags & 0x70) >> 4) + 1
    bitmap_obj = bitmap(w, h, (1 << color_bits) - 1)
    while True:
        block_type = file.read(1)[0]
        if block_type == 0x2c: # frame
            dx, dy, frame_w, frame_h, flags = struct.unpack('<HHHHB',
                                                          file.read(9))
            if (flags & 0x40) != 0:
                raise NotImplementedError("Interlacing not supported")
            if (flags & 0x80) != 0:
                palette_size = 1 << ((flags & 0x07) + 1)
                frame_palette = palette(palette_size)
                for i in range(palette_size):
                    frame_palette[i] = file.read(3)
                if palette_obj is None:
                    # if there is no global palette, use local one
                    palette_obj = frame_palette
            min_code_size = file.read(1)[0]
            x = 0
            y = 0
            for decoded in lzw_decode(_read_blockstream(file), min_code_size):
                for byte in decoded:
                    bitmap_obj[dx+x, dy+y] = byte
                    x += 1
                    if x >= frame_w:
                        x = 0
                        y += 1
        elif block_type == 0x21: # extension
            extension_type = file.read(1)[0]
            # 0x01 = label, 0xfe = comment
            data = bytes(_read_blockstream(file))
        elif block_type == 0x3b: # terminator
            break
        else:
            raise ValueError("Bad block type")
    return bitmap_obj, palette_obj


def _read_blockstream(f):
    while True:
        size = f.read(1)[0]
        if size == 0:
            break
        for i in range(size):
            yield f.read(1)[0]


class EndOfData(Exception):
    pass


class LZWDict:
    def __init__(self, code_size):
        self.code_size = code_size
        self.clear_code = 1 << code_size
        self.end_code = self.clear_code + 1
        self.codes = []
        self.clear()

    def clear(self):
        self.last = b''
        self.code_len = self.code_size + 1
        self.codes[:] = []

    def decode(self, code):
        if code == self.clear_code:
            self.clear()
            return b''
        elif code == self.end_code:
            raise EndOfData()
        elif code < self.clear_code:
            value = bytes([code])
        elif code <= len(self.codes) + self.end_code:
            value = self.codes[code - self.end_code - 1]
        else:
            value = self.last + self.last[0:1]
        if self.last:
            self.codes.append(self.last + value[0:1])
        if (len(self.codes) + self.end_code + 1 >= 1 << self.code_len and
            self.code_len < 12):
                self.code_len += 1
        self.last = value
        return value


def lzw_decode(data, code_size):
    dictionary = LZWDict(code_size)
    bit = 0
    byte = next(data)
    try:
        while True:
            code = 0
            for i in range(dictionary.code_len):
                code |= ((byte >> bit) & 0x01) << i
                bit += 1
                if bit >= 8:
                    bit = 0
                    byte = next(data)
            yield dictionary.decode(code)
    except EndOfData:
        while True:
            next(data)
