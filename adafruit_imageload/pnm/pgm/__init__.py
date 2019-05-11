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
#import logging

def load(file, magic_number, header, *, bitmap=None, palette=None):
    if header[2] > 256:
        raise NotImplementedError("16 bit files are not supported")
    width = header[0]
    height = header[1]

    data_start = file.tell()  # keep this so we can rewind
    #bitmap = bitmap(width, height, max_colors)
    palette_colors = set()

    if magic_number == b'P2':  # To handle ascii PGM files.
        # Handle ascii

        pixel = bytearray()
        byte = True
        # scan all colors present in the file
        while byte:
            byte = file.read(1)  # type: byte
            if not byte.isdigit():
                int_pixel = int("".join(["%c" % char for char in pixel]))
                #logging.info(f'color {pixel} {int_pixel}')
                #bitmap[x, y] = int_pixel
                palette_colors.add(int_pixel)
                pixel = bytearray()
            pixel += byte

        # logging.info(f'{x}, {y}, {byte}, {int_pixel}')
        if palette:
            palette = palette(len(palette_colors))
            for counter, color in enumerate(palette_colors):
                palette[counter] = bytes([color, color, color])
        if bitmap:
            bitmap = bitmap(width, height, len(palette_colors))
            palette_colors = list(palette_colors)
            file.seek(data_start)
            for y in range(height):
                for x in range(width):
                    pixel = bytearray()
                    # Takes int and converts to an 8 bit
                    while True:
                        byte = file.read(1)  # type: byte
                        if not byte.isdigit():
                            break
                        pixel += byte
                    # convert b'255' to b'\xff'
                    color = int("".join(["%c" % char for char in pixel]))
                    #logging.info(f'found color {color} in palette at {palette_colors.index(color)}')
                    bitmap[x, y] = palette_colors.index(color)

        return bitmap, palette

    if magic_number == b'P5':  # To handle binary PGM files.
        for y in range(height):
            for x in range(width):
                byte = file.read(1)
                if byte == b"":
                    raise ValueError("ran out of file unexpectedly")
                int_pixel = int.from_bytes(byte, "little")
                bitmap[x, y] = int_pixel
                palette_colors.add(int_pixel)

        if palette:
            palette = palette(len(palette_colors))
            for counter, color in enumerate(palette_colors):
                color_bytearray = bytearray()
                for i in range(3):
                    color_bytearray += bytes([color])
                palette[counter] = color_bytearray

        return bitmap, palette

    raise NotImplementedError("Was not able to send image")
