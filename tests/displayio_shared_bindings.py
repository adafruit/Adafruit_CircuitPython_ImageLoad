# The MIT License (MIT)
#
# Copyright (c) 2019 Matt Land
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
`adafruit_imageload.tests.displayio_shared_bindings`
====================================================

The classes in this file are designed to emulate Circuitpython's displayio classes
for Bitmap and Palette. These mimic classes should have the same methods and interface as the real interface,
but with extra validation checks, warnings, and messages to facilitate debugging.

Code that can be run successfully against these classes will have a good chance of
 working correctly on hardware running Circuitpython, but without needing to upload code to a board
 after each attempt.

* Author(s):  Matt Land

"""
from typing import Union


class Bitmap_C_Interface(object):
    """
    A class to simulate the displayio.Bitmap class for testing, based on
    https://circuitpython.readthedocs.io/en/latest/shared-bindings/displayio/Bitmap.html
    In case of discrepancy, the C implementation takes precedence.
    """

    def __init__(self, width: int, height: int, colors: int) -> None:
        self.width = width
        self.height = height
        self.colors = colors
        self.data = {}

    def _abs_pos(self, width: int, height: int) -> int:
        if height >= self.height:
            raise ValueError("height > max")
        if width >= self.width:
            raise ValueError("width > max")
        return width + (height * self.width)

    def _decode(self, position: int) -> tuple:
        return position % self.width, position // self.width

    def __setitem__(self, key: Union[tuple, int], value: int) -> None:
        """
        Set using x, y coordinates, or absolution position
        bitmap[0] = 1
        bitmap[2,1] = 5
        """
        if isinstance(key, tuple):
            # order is X, Y from the docs
            # https://github.com/adafruit/circuitpython/blob/master/shared-bindings/displayio/Bitmap.c
            self.__setitem__(self._abs_pos(key[0], key[1]), value)
            return
        if not isinstance(value, (int)):
            raise RuntimeError(f"set value as int, not {type(value)}")
        if value > 255:
            raise ValueError(f"pixel value {value} too large")
        if self.data.get(key):
            raise ValueError(
                f"pixel {self._decode(key)}/{key} already set, cannot set again"
            )
        self.data[key] = value

    def __getitem__(self, item: Union[tuple, int]) -> bytearray:
        if isinstance(item, tuple):
            return self.__getitem__(self._abs_pos(item[0], item[1]))
        if item > self.height * self.width:
            raise RuntimeError(f"get position out of range {item}")
        try:
            return self.data[item]
        except KeyError:
            raise RuntimeError("no data at {} [{}]".format(self._decode(item), item))

    def validate(self, detect_empty_image=True) -> None:
        """
        method to to make sure all pixels allocated in the Bitmap
        were set with a value
        """
        seen_colors = set()
        if not self.data:
            raise ValueError("no rows were set / no data in memory")
        for y in range(self.height):
            for x in range(self.width):
                try:
                    seen_colors.add(self[x, y])
                except KeyError:
                    raise ValueError(f"missing data at {x},{y}")
        if detect_empty_image and len(seen_colors) < 2:
            raise ValueError(
                "image detected as only one color. set detect_empty_image=False to ignore"
            )

    def __str__(self) -> str:
        """
        method to dump the contents of the Bitmap to a terminal,
        for debugging purposes

        Example:
        --------

        bitmap = Bitmap(5, 4, 4)
        ...  # assign bitmap values
        print(str(bitmap))
        """
        out = "\n"
        for y in range(self.height):
            for x in range(self.width):
                data = self[x, y]
                out += f"{data:>4}"
            out += "\n"
        return out


class Palette_C_Interface(object):
    """
    A class to simulates the displayio.Palette class for testing, based on
    https://circuitpython.readthedocs.io/en/latest/shared-bindings/displayio/Palette.html
    In case of discrepancy, the C implementation takes precedence.
    """

    def __init__(self, num_colors: int) -> None:
        self.num_colors = num_colors
        self.colors = {}

    def __setitem__(self, key: int, value: Union[bytes, int, bytearray]) -> None:
        """
        Set using zero indexed color value
        palette = Palette(1)
        palette[0] = 0xFFFFFF

        """
        if key >= self.num_colors:
            raise ValueError(
                f"palette index {key} is greater than allowed by num_colors {self.num_colors}"
            )
        if not isinstance(value, (bytes, int, bytearray)):
            raise ValueError(f"palette color should be bytes, not {type(value)}")
        if isinstance(value, int) and value > 0xFFFFFF:
            raise ValueError(f"palette color int {value} is too large")
        if self.colors.get(key):
            raise ValueError(
                f"palette color {key} was already set, should not reassign"
            )
        self.colors[key] = value

    def __getitem__(self, item: int) -> Union[bytes, int, bytearray]:
        """
        Warning: this method is not supported in the actual C interface.
        It is provided here for debugging purposes.
        """
        if item >= self.num_colors:
            raise ValueError(
                f"palette index {item} should be less than {self.num_colors}"
            )
        if not self.colors.get(item):
            raise ValueError(f"palette index {item} is not set")
        return self.colors[item]

    def validate(self):
        """
        method to make sure all colors allocated in Palette were set to a value
        """
        if not self.colors:
            raise IndexError("no palette colors were set")
        if len(self.colors) != self.num_colors:
            raise IndexError(
                "palette was initialized for {} colors, but only {} were inserted".format(
                    self.num_colors, len(self.colors)
                )
            )
        for i in range(self.num_colors):
            try:
                self.colors
            except IndexError:
                raise ValueError("missing color `{}` in palette color list".format(i))

    def __str__(self):
        """
        method to dump the contents of the Palette to a terminal,
        for debugging purposes

        Example:
        --------

        palette = Palette(1)
        palette[0] = 0xFFFFFF
        print(str(palette))
        """
        out = "\nPalette:\n"
        for y in range(len(self.colors)):
            out += f" [{y}] {self.colors[y]}\n"
        return out
