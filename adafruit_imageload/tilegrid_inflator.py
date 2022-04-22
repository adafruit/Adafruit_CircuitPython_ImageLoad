# SPDX-FileCopyrightText: 2022 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_imageload.tilegrid_inflator`
====================================================

Use a 3x3 spritesheet to inflate a larger grid of tiles, duplicating the center rows and
columns as many times as needed to reach a target size.

* Author(s): Tim Cocks

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad.git"

import displayio
import adafruit_imageload


def inflate_tilegrid(
    bmp_path=None,
    target_size=(3, 3),
    tile_size=None,
    transparent_index=None,
    bmp_obj=None,
    bmp_palette=None,
):
    """
    inflate a TileGrid of ``target_size`` in tiles from a 3x3 spritesheet by duplicating
    the center rows and columns.

    :param string bmp_path: filepath to the 3x3 spritesheet bitmap file
    :param tuple target_size: desired size in tiles (target_width, target_height)
    :param Optional[tuple] tile_size: size of the tiles in the 3x3 spritesheet. If
      None is used it will equally divide the width and height of the Bitmap by 3.
    :param Union[tuple, int] transparent_index: a single index within the palette to
      make transparent, or a tuple of multiple indexes to make transparent
    :param OnDiskBitmap bmp_obj: Already loaded 3x3 spritesheet in an OnDiskBitmap
    :param Palette bmp_palette: Already loaded spritesheet Palette
    """

    # pylint: disable=too-many-arguments, too-many-locals, too-many-branches

    if bmp_path is None and (bmp_obj is None and bmp_palette is None):
        raise AttributeError("Must pass either bmp_path or bmp_obj and bmp_palette")

    if bmp_path is not None:
        image, palette = adafruit_imageload.load(bmp_path)
    else:
        image = bmp_obj
        palette = bmp_palette

    if transparent_index is not None:
        if isinstance(transparent_index, tuple):
            for index in transparent_index:
                palette.make_transparent(index)
        elif isinstance(transparent_index, int):
            palette.make_transparent(transparent_index)

    if tile_size is None:
        tile_width = image.width // 3
        tile_height = image.height // 3
    else:
        tile_width = tile_size[0]
        tile_height = tile_size[1]

    target_width = target_size[0]
    target_height = target_size[1]

    tile_grid = displayio.TileGrid(
        image,
        pixel_shader=palette,
        height=target_height,
        width=target_width,
        tile_width=tile_width,
        tile_height=tile_height,
    )

    # corners
    tile_grid[0, 0] = 0  # upper left
    tile_grid[tile_grid.width - 1, 0] = 2  # upper right
    tile_grid[0, tile_grid.height - 1] = 6  # lower left
    tile_grid[tile_grid.width - 1, tile_grid.height - 1] = 8  # lower right

    for x in range(target_size[0] - 2):
        tile_grid[x + 1, 0] = 1
        tile_grid[x + 1, tile_grid.height - 1] = 7

    for y in range(target_size[1] - 2):
        tile_grid[0, y + 1] = 3
        tile_grid[tile_grid.width - 1, y + 1] = 5

    for y in range(target_size[1] - 2):
        for x in range(target_size[0] - 2):
            tile_grid[x + 1, y + 1] = 4

    return tile_grid