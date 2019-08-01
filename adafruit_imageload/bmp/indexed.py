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
`adafruit_imageload.bmp.indexed`
====================================================

Load pixel values (indices or colors) into a bitmap and colors into a palette from an indexed BMP.

* Author(s): Scott Shawcroft

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad.git"

def load(file, width, height, data_start, colors, color_depth, *, bitmap=None, palette=None):
    """Loads indexed bitmap data into bitmap and palette objects.

       :param file file: The open bmp file
       :param int width: Image width in pixels
       :param int height: Image height in pixels
       :param int data_start: Byte location where the data starts (after headers)
       :param int colors: Number of distinct colors in the image
       :param int color_depth: Number of bits used to store a value"""
    # pylint: disable=too-many-arguments,too-many-locals
    if palette:
        palette = palette(colors)

        file.seek(data_start - colors * 4)
        for value in range(colors):
            c_bytes = file.read(4)
            # Need to swap red & blue bytes (bytes 0 and 2)
            palette[value] = bytes(b''.join([c_bytes[2:3],
                                             c_bytes[1:2],
                                             c_bytes[0:1],
                                             c_bytes[3:1]]))

    if bitmap:
        minimum_color_depth = 1
        while colors > 2 ** minimum_color_depth:
            minimum_color_depth *= 2

        #convert unsigned int to signed int when height is negative
        if height > 0x7fffffff:
    		height = height - 4294967296
        theight = height
        if theight < 0:
            theight = 0 - theight
        bitmap = bitmap(width, theight, colors)
        file.seek(data_start)
        line_size = width // (8 // color_depth)
        if width % (8 // color_depth) != 0:
            line_size += 1
        if line_size % 4 != 0:
            line_size += (4 - line_size % 4)

        chunk = bytearray(line_size)
        mask = (1 << minimum_color_depth) - 1
        if height > 0:
            range1 = height - 1
            range2 = -1
            range3 = -1
        else:
            range1 = 0
            range2 = abs(height)
            range3 = 1
        for y in range(range1, range2, range3):
            file.readinto(chunk)
            pixels_per_byte = 8 // color_depth
            offset = y * width

            for x in range(width):
                i = x // pixels_per_byte
                pixel = (chunk[i] >> (8 - color_depth*(x % pixels_per_byte + 1))) & mask
                bitmap[offset + x] = pixel

    return bitmap, palette
