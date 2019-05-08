from unittest import TestCase
from adafruit_imageload import pnm
from io import BytesIO
import logging
import os


class Bitmap_C_Interface(object):
    def __init__(self, width, height, colors):
        self.width = width
        self.height = height
        self.colors = colors
        self.data = {}

    def _abs_pos(self, width, height):
        if height > self.height - 1:
            raise ValueError("height > max")
        if width > self.width - 1:
            raise ValueError("width > max")
        return (width * self.width) + height

    def _decode(self, position):
        return position // self.width, position % self.width

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            # order is X, Y from the docs https://github.com/adafruit/circuitpython/blob/master/shared-bindings/displayio/Bitmap.c
            self.__setitem__(self._abs_pos(key[0], key[1]), value)
            return
        # if key > self.height * self.width:
        #    raise RuntimeError('illegal set position {}'.format(self._decode(key)))
        if not isinstance(value, int):
            raise RuntimeError(f"set value as int, not {type(value)}")
        self.data[key] = value

    def __getitem__(self, item: str) -> bytearray:
        if isinstance(item, tuple):
            return self.__getitem__(self._abs_pos(item[0], item[1]))
        # if item > self.height * self.width:
        #    raise RuntimeError('illegal item position {}'.format(item))
        try:
            return self.data[item]
        except KeyError:
            raise RuntimeError("no data at {}".format(self._decode(item)))

    def validate(self):
        if not self.data:
            raise ValueError("no rows were set / no data in memory")
        for i in range(self.height * self.width, 1):
            try:
                self.data[i]
            except KeyError:
                raise ValueError("missing data at {i}")

    def __str__(self):
        out = "\n"
        for y in range(self.height):
            for x in range(self.width):
                data = self[x, y]
                out += f"{data}"
            out += "\n"
        return out


logging.getLogger().setLevel(logging.INFO)


class TestBitmap_C(TestCase):
    def test_init(self):
        b = Bitmap_C_Interface(2, 4, 1)
        self.assertEqual(2, b.width)
        self.assertEqual(4, b.height)
        self.assertEqual(1, b.colors)

    def test_set_tuple(self):
        b = Bitmap_C_Interface(2, 4, 1)
        b[0, 0] = 67
        self.assertEqual(b[0, 0], 67)

    def test_set_abs(self):
        b = Bitmap_C_Interface(2, 4, 1)
        b[0] = 42
        self.assertEqual(b[0], 42)

    def test_abs_and_tuple(self):
        b = Bitmap_C_Interface(2, 4, 1)
        b[0] = 101
        self.assertEqual(101, b[0, 0])

    def test_non_zero(self):
        b = Bitmap_C_Interface(2, 4, 1)
        b[1, 1] = 100
        self.assertEqual(100, b[1, 1])

    def test_throws_x_out_of_range(self):
        b = Bitmap_C_Interface(2, 4, 1)
        try:
            b[2, 1] = 100
            self.fail("should have thrown")
        except ValueError:
            pass

    def test_max(self):
        b = Bitmap_C_Interface(2, 4, 1)
        b[1, 1] = 66
        self.assertEqual(66, b[1, 1])

    def test_uninitialized(self):
        b = Bitmap_C_Interface(2, 4, 1)
        try:
            b[1, 1]
            self.fail("should have thrown")
        except RuntimeError:
            pass

    def test_validate_throws(self):
        b = Bitmap_C_Interface(2, 4, 1)
        try:
            b.validate()
        except ValueError:
            pass

    def test_repr(self):
        b = Bitmap_C_Interface(3, 2, 1)
        b[0, 0] = 1
        b[1, 0] = 0
        b[2, 0] = 0
        b[0, 1] = 1
        b[1, 1] = 1
        b[2, 1] = 0
        self.assertEqual("\n100\n110\n", str(b))

    def test_decode(self):
        b = Bitmap_C_Interface(4, 4, 1)
        self.assertEqual((0, 0), b._decode(0))
        encoded = b._abs_pos(3, 3)
        self.assertEqual((3, 3), b._decode(encoded))


class TestPnmLoad(TestCase):
    def test_load_fails_with_no_header_data(self):
        f = BytesIO(b"some initial binary data: \x00\x01")
        try:
            pnm.load(f, b"P1", bitmap=Bitmap_C_Interface)
            self.fail("should have failed")
        except Exception as e:
            if "Unsupported image format" not in str(e):
                raise

    def test_load_works_p1_ascii(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "examples",
            "images",
            "netpbm_p1_mono.pbm",
        )
        with open(test_file, "rb") as f:
            bitmap, palette = pnm.load(f, b"P1", bitmap=Bitmap_C_Interface)
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(13, bitmap.width)
        self.assertEqual(21, bitmap.height)

        bitmap.validate()
        self.assertEqual(0, bitmap[0])  # check first row
        self.assertEqual(1, bitmap[12, 1])  # check second row

    def test_load_works_p4_in_mem(self):
        f = BytesIO(b"P4\n4 2\n\x55")
        bitmap, palette = pnm.load(f, b"P4", bitmap=Bitmap_C_Interface)
        self.assertEqual(4, bitmap.width)
        self.assertEqual(2, bitmap.height)
        bitmap.validate()
        self.assertEqual("\n1010\n1010\n", str(bitmap))

    def test_load_works_p4_binary(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "examples",
            "images",
            "netpbm_p4_mono.pbm",
        )
        with open(test_file, "rb") as f:
            bitmap, palette = pnm.load(f, b"P4", bitmap=Bitmap_C_Interface)
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface))
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(8, bitmap.width)
        self.assertEqual(8, bitmap.height)
        bitmap.validate()

    def test_load_works_p4_binary_high_res(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "examples",
            "images",
            "netpbm_p4_mono_large.pbm",
        )
        with open(test_file, "rb") as f:
            bitmap, palette = pnm.load(f, b"P4", bitmap=Bitmap_C_Interface)
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface))
        self.assertEqual(1, bitmap.colors)
        self.assertEqual(1920, bitmap.width)
        self.assertEqual(1080, bitmap.height)


class TestPPMLoad(TestCase):
    def test_load_works_p3_ascii(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "examples",
            "images",
            "netpbm_p3_rgb_ascii.ppm",
        )
        with open(test_file, "rb") as f:
            bitmap, palette = pnm.load(f, b"P3", bitmap=Bitmap_C_Interface)
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)
        self.assertEqual(16777216, bitmap.colors)
        self.assertEqual(16, bitmap.width)
        self.assertEqual(16, bitmap.height)
        bitmap.validate()
        str(bitmap)

    def test_load_works_p6_binary(self):
        test_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "examples",
            "images",
            "netpbm_p6_binary.ppm",
        )
        with open(test_file, "rb") as f:
            bitmap, palette = pnm.load(f, b"P6", bitmap=Bitmap_C_Interface)
        self.assertTrue(isinstance(bitmap, Bitmap_C_Interface), bitmap)
        self.assertEqual(16777216, bitmap.colors)
        self.assertEqual(16, bitmap.width)
        self.assertEqual(16, bitmap.height)
        bitmap.validate()
        str(bitmap)
