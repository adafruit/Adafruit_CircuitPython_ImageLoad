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


def load(file, magic_number, header, *, bitmap=None, palette=None):
    # TODO: remove unused variables later
    width = header[0]
    height = header[1]
    max_colors = header[2]
    min_color = 1 # probably don't need this
    columns = height
    bitmap = bitmap(width, height, max_colors)


    if max_colors > 256:
        # raise exception
        raise NotImplementedError("16 bit grayscale not supported")

    if magic_number == b'P2':
        # Handle ascii
        colors = set()
        for y in range(height):
            for x in range(width):
            # Takes int and converts to an 8 bit
                pixel = bytearray()

                while True:
                    bit = file.read(1)  # type: byte
                    if not bit.isdigit():
                        break
                    pixel += bit

                int_pixel = int("".join(["%c" % char for char in pixel]))
                bitmap[x, y] = int_pixel
                colors.add(int_pixel)
        if palette:
            palette = palette(len(colors))
            for counter, color in enumerate(colors):
                color_bytearray = bytearray()
                for i in range(3):
                    color_bytearray += bytes([color])
                palette[counter] = color_bytearray
        return bitmap, palette


    if magic_number == b'P5':
        raise NotImplementedError("This is a Binary file")

    raise NotImplementedError("Was not able to send image")