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


def load(file, magic_number, header, *, bitmap=None, palette=None):
    """
    Perform the load of Netpbm greyscale images
    :param file: stream resource with the pointer at the start of data
    :param magic_number: string P2 or P6
    :param header: list of width, height, max color value
    :param bitmap: displayio.Bitmap class object
    :param palette: displayio.Palette class object
    :return:
    """
    if header[2] > 256:
        raise NotImplementedError("16 bit files are not supported")
    width = header[0]
    height = header[1]

    data_start = file.tell()  # keep this so we can rewind
    palette_colors = set()

    if magic_number == b"P2":  # To handle ascii PGM files.
        pixel = bytearray()
        # build a set of all colors present in the file, so palette and bitmap can be constructed
        while True:
            byte = file.read(1)
            if byte == b"":
                break
            if not byte.isdigit():
                int_pixel = int("".join(["%c" % char for char in pixel]))
                palette_colors.add(int_pixel)
                pixel = bytearray()
            pixel += byte
        if palette:
            palette = build_palette(palette, palette_colors)
        if bitmap:
            bitmap = bitmap(width, height, len(palette_colors))
            palette_colors = list(palette_colors)
            file.seek(data_start)
            for y in range(height):
                for x in range(width):
                    pixel = bytearray()
                    while True:
                        byte = file.read(1)
                        if not byte.isdigit():
                            break
                        pixel += byte
                    int_pixel = int("".join(["%c" % char for char in pixel]))
                    bitmap[x, y] = palette_colors.index(int_pixel)
        return bitmap, palette

    if magic_number == b"P5":  # To handle binary PGM files.
        for y in range(height):
            data_line = iter(bytes(file.read(width)))
            for pixel in data_line:
                palette_colors.add(pixel)

        if palette:
            palette = build_palette(palette, palette_colors)
        if bitmap:
            bitmap = bitmap(width, height, len(palette_colors))
            palette_colors = list(palette_colors)
            file.seek(data_start)
            for y in range(height):
                data_line = iter(bytes(file.read(width)))
                for x, pixel in enumerate(data_line):
                    bitmap[x, y] = palette_colors.index(pixel)
        return bitmap, palette

    raise NotImplementedError("Was not able to send image")


def build_palette(palette_class, palette_colors):
    palette = palette_class(len(palette_colors))
    for counter, color in enumerate(palette_colors):
        palette[counter] = bytes([color, color, color])
    return palette
