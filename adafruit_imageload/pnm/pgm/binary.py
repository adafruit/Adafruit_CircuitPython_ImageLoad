# SPDX-FileCopyrightText: 2018 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: 2022 Matt Land
# SPDX-FileCopyrightText: Brooke Storm
# SPDX-FileCopyrightText: Sam McGahan
#
# SPDX-License-Identifier: MIT

"""
`adafruit_imageload.pnm.pgm.binary`
====================================================

Load pixel values (indices or colors) into a bitmap and colors into a palette.

* Author(s): Matt Land, Brooke Storm, Sam McGahan

"""
try:
    from typing import Tuple, Optional, Set, List
    from io import BufferedReader
    from displayio import Palette, Bitmap
    from ...displayio_types import PaletteConstructor, BitmapConstructor
except ImportError:
    pass


def load(
    file: BufferedReader,
    width: int,
    height: int,
    bitmap: BitmapConstructor = None,
    palette: PaletteConstructor = None,
) -> Tuple[Optional[Bitmap], Optional[Palette]]:
    """
    Load a P5 format file (binary), handle PGM (greyscale)
    """
    palette_colors = set()  # type: Set[int]
    data_start = file.tell()
    for y in range(height):
        data_line = iter(bytes(file.read(width)))
        for pixel in data_line:
            palette_colors.add(pixel)

    if palette:
        palette = build_palette(palette, palette_colors)  # type: Palette
    if bitmap:
        bitmap = bitmap(width, height, len(palette_colors))  # type: Bitmap
        palette_colors = list(palette_colors)  # type: List[int]
        file.seek(data_start)
        for y in range(height):
            data_line = iter(bytes(file.read(width)))
            for x, pixel in enumerate(data_line):
                bitmap[x, y] = palette_colors.index(pixel)
    return bitmap, palette


def build_palette(
    palette_class: PaletteConstructor, palette_colors: Set[int]
) -> Palette:
    """
    construct the Palette, and populate it with the set of palette_colors
    """
    _palette = palette_class(len(palette_colors))
    for counter, color in enumerate(palette_colors):
        _palette[counter] = bytes([color, color, color])
    return _palette
