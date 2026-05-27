# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_imageload.tests.test_bmp_truecolor_load`
==================================================

Regression coverage for ``adafruit_imageload.bmp.truecolor``.

The original loader did not honour the 4-byte scan-line padding that the
BMP format requires, so 24-bit BMPs whose ``width * 3`` is not a multiple
of 4 (e.g. 125x125) loaded with row drift and scrambled colors.

* Author(s): Melissa LeBlanc-Williams

"""

import os
import struct
import tempfile
from unittest import TestCase

from adafruit_imageload import load

from .displayio_shared_bindings import Bitmap_C_Interface


def _write_truecolor_bmp(path, pixels_topdown, width, height):
    """Write a 24-bit BMP with the given top-down RGB888 pixel list.

    ``pixels_topdown`` is a flat list of (R, G, B) tuples in row-major
    top-down order (i.e. the first ``width`` entries are the top row).
    The BMP file itself stores rows bottom-up with 4-byte row padding.
    """
    row_bytes = width * 3
    pad = (4 - row_bytes % 4) % 4
    data = bytearray()
    # BMP rows are stored bottom-up.
    for row_idx in range(height - 1, -1, -1):
        row_start = row_idx * width
        for px in range(width):
            r, g, b = pixels_topdown[row_start + px]
            # BMP byte order is B, G, R.
            data.extend((b, g, r))
        data.extend(b"\x00" * pad)

    dib = struct.pack(
        "<IiiHHIIiiII",
        40,  # DIB header size (BITMAPINFOHEADER)
        width,
        height,  # positive => bottom-up storage
        1,  # planes
        24,  # bpp
        0,  # BI_RGB (no compression)
        len(data),
        2835,
        2835,
        0,
        0,
    )
    data_offset = 14 + 40
    file_size = data_offset + len(data)
    hdr = b"BM" + struct.pack("<IHHI", file_size, 0, 0, data_offset)
    with open(path, "wb") as fp:
        fp.write(hdr + dib + data)


# RGB888 colors used in the fixtures.
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Their RGB565 representations (R5 G6 B5).
RGB565_RED = 0xF800
RGB565_GREEN = 0x07E0
RGB565_BLUE = 0x001F
RGB565_WHITE = 0xFFFF
RGB565_BLACK = 0x0000
RGB565_YELLOW = 0xFFE0


class TestBmpTruecolorLoad(TestCase):
    def test_24bit_no_row_padding(self):
        """Width 4 -> row stride 12 bytes, already 4-byte aligned."""
        # 4x2 image, row 0 (top): RED GREEN BLUE WHITE
        #           row 1 (bot): BLACK YELLOW RED GREEN
        pixels = [RED, GREEN, BLUE, WHITE, BLACK, YELLOW, RED, GREEN]
        with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as tmp:
            path = tmp.name
        try:
            _write_truecolor_bmp(path, pixels, 4, 2)
            bitmap, _ = load(file_or_filename=path, bitmap=Bitmap_C_Interface)
        finally:
            os.unlink(path)

        self.assertEqual(4, bitmap.width)
        self.assertEqual(2, bitmap.height)
        expected = [
            RGB565_RED,
            RGB565_GREEN,
            RGB565_BLUE,
            RGB565_WHITE,
            RGB565_BLACK,
            RGB565_YELLOW,
            RGB565_RED,
            RGB565_GREEN,
        ]
        for idx, want in enumerate(expected):
            x, y = idx % 4, idx // 4
            self.assertEqual(
                want, bitmap[x, y], f"pixel ({x},{y}) want 0x{want:04x} got 0x{bitmap[x, y]:04x}"
            )

    def test_24bit_row_padding_required(self):
        """Width 3 -> row stride 9 bytes, needs 3 bytes of padding per row.

        This is the regression test: prior to the fix, the second row read
        would slide into the first row's padding bytes and the rest of the
        image, scrambling all subsequent rows.
        """
        # 3x2 image, row 0 (top): WHITE BLACK YELLOW
        #           row 1 (bot): RED   GREEN BLUE
        pixels = [WHITE, BLACK, YELLOW, RED, GREEN, BLUE]
        with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as tmp:
            path = tmp.name
        try:
            _write_truecolor_bmp(path, pixels, 3, 2)
            bitmap, _ = load(file_or_filename=path, bitmap=Bitmap_C_Interface)
        finally:
            os.unlink(path)

        self.assertEqual(3, bitmap.width)
        self.assertEqual(2, bitmap.height)
        expected = [
            RGB565_WHITE,
            RGB565_BLACK,
            RGB565_YELLOW,
            RGB565_RED,
            RGB565_GREEN,
            RGB565_BLUE,
        ]
        for idx, want in enumerate(expected):
            x, y = idx % 3, idx // 3
            self.assertEqual(
                want, bitmap[x, y], f"pixel ({x},{y}) want 0x{want:04x} got 0x{bitmap[x, y]:04x}"
            )

    def test_24bit_odd_width_taller(self):
        """Width 5 -> row stride 15 bytes, needs 1 byte of padding per row.

        Uses 3 rows so any drift would compound, catching off-by-one fixes
        that happen to work for 2-row inputs.
        """
        # 5x3, top-down:
        #  row 0: RED   GREEN BLUE  WHITE BLACK
        #  row 1: YELLOW RED   GREEN BLUE  WHITE
        #  row 2: BLACK YELLOW RED   GREEN BLUE
        pixels = [
            RED,
            GREEN,
            BLUE,
            WHITE,
            BLACK,
            YELLOW,
            RED,
            GREEN,
            BLUE,
            WHITE,
            BLACK,
            YELLOW,
            RED,
            GREEN,
            BLUE,
        ]
        with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as tmp:
            path = tmp.name
        try:
            _write_truecolor_bmp(path, pixels, 5, 3)
            bitmap, _ = load(file_or_filename=path, bitmap=Bitmap_C_Interface)
        finally:
            os.unlink(path)

        self.assertEqual(5, bitmap.width)
        self.assertEqual(3, bitmap.height)
        expected_565 = [
            RGB565_RED,
            RGB565_GREEN,
            RGB565_BLUE,
            RGB565_WHITE,
            RGB565_BLACK,
            RGB565_YELLOW,
            RGB565_RED,
            RGB565_GREEN,
            RGB565_BLUE,
            RGB565_WHITE,
            RGB565_BLACK,
            RGB565_YELLOW,
            RGB565_RED,
            RGB565_GREEN,
            RGB565_BLUE,
        ]
        for idx, want in enumerate(expected_565):
            x, y = idx % 5, idx // 5
            self.assertEqual(
                want, bitmap[x, y], f"pixel ({x},{y}) want 0x{want:04x} got 0x{bitmap[x, y]:04x}"
            )
