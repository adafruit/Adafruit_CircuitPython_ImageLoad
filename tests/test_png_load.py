# SPDX-FileCopyrightText: 2025 Tim Cocks for Adafruit Industries
# SPDX-License-Identifier: MIT

from unittest import TestCase

from adafruit_imageload import load


class TestPngLoad(TestCase):
    def test_expected_pixels(self):
        img, palette = load("tests/test_png.png")
        self.assertEqual(len(palette), 3)
        self.assertEqual(img.width, 4)
        self.assertEqual(img.height, 4)

        self.assertEqual(img[0, 0], 0)
        self.assertEqual(img[1, 0], 2)
        self.assertEqual(img[2, 0], 1)
        self.assertEqual(img[3, 0], 0)

        self.assertEqual(img[0, 3], 0)
        self.assertEqual(img[1, 3], 2)
        self.assertEqual(img[2, 3], 1)
        self.assertEqual(img[3, 3], 0)
