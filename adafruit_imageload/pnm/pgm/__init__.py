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

                bitmap[x, y] = int(pixel)
                colors.add(int(pixel))
        if palette:
            palette = palette(len(colors))
            for counter, color in enumerate(colors):
                color_int = int(f'{hex(color)}{hex(color)[2:]}{hex(color)[2:]}', 16) # HACK: is there a better way?
                palette[counter] = color_int
        return bitmap, palette


    if magic_number == b'P5':
        raise NotImplementedError("Nope")

    raise NotImplementedError("no")

    # Assign bits to bitmap

        # create pallete

        # create bitmap

        # Loop through lines using line width and build

        # Return bitmap

    # Example bitmap object:
        # [
        #   [(222), (33), (5), (76), (55), (82)]
        # ]



    # if bitmap:
    #     minimum_color_depth = 1
    #     while colors > 2 ** minimum_color_depth:
    #         minimum_color_depth *= 2

    #     bitmap = bitmap(width, height, colors)
    #     f.seek(data_start)
    #     line_size = width // (8 // color_depth)
    #     if line_size % 4 != 0:
    #         line_size += (4 - line_size % 4)

    #     packed_pixels = None
    #     if color_depth != minimum_color_depth and minimum_color_depth == 2:
    #         target_line_size = width // 4
    #         if target_line_size % 4 != 0:
    #             target_line_size += (4 - target_line_size % 4)

    #         packed_pixels = bytearray(target_line_size)

    #     for line in range(height-1,-1,-1):
    #         chunk = f.read(line_size)
    #         if packed_pixels:
    #             original_pixels_per_byte = 8 // color_depth
    #             packed_pixels_per_byte = 8 // minimum_color_depth

    #             for i in range(width // packed_pixels_per_byte):
    #                 packed_pixels[i] = 0

    #             for i in range(width):
    #                 pi = i // packed_pixels_per_byte
    #                 ci = i // original_pixels_per_byte
    #                 packed_pixels[pi] |= ((chunk[ci] >> (8 - color_depth*(i % original_pixels_per_byte + 1))) & 0x3) << (8 - minimum_color_depth*(i % packed_pixels_per_byte + 1))

    #             bitmap._load_row(line, packed_pixels)
    #         else:
    #             bitmap._load_row(line, chunk)

    # return bitmap, palette