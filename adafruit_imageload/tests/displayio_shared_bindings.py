class Bitmap_C_Interface(object):
    """
    Simulates the displayio.Bitmap class for testing
    """

    def __init__(self, width, height, colors):
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

    def __setitem__(self, key: tuple, value: int):
        if isinstance(key, tuple):
            # order is X, Y from the docs https://github.com/adafruit/circuitpython/blob/master/shared-bindings/displayio/Bitmap.c
            self.__setitem__(self._abs_pos(key[0], key[1]), value)
            return
        if not isinstance(value, (int)):
            raise RuntimeError(f"set value as int, not {type(value)}")
        if value > 255:
            raise ValueError(f"pixel value {value} too large")
        self.data[key] = value

    def __getitem__(self, item: tuple) -> bytearray:
        if isinstance(item, tuple):
            return self.__getitem__(self._abs_pos(item[0], item[1]))
        if item > self.height * self.width:
            raise RuntimeError(f"get position out of range {item}")
        try:
            return self.data[item]
        except KeyError:
            raise RuntimeError("no data at {} [{}]".format(self._decode(item), item))

    def validate(self):
        if not self.data:
            raise ValueError("no rows were set / no data in memory")
        for i in range(self.height * self.width, 0):
            try:
                self.data[i]
            except KeyError:
                raise ValueError("missing data at {i}")

    def __str__(self):
        out = "\n"
        for y in range(self.height):
            for x in range(self.width):
                data = self[x, y]
                out += f"{data:>4}"
            out += "\n"
        return out


class Palette_C_Interface(object):
    """
    Simulates the displayio.Palette class for testing
    """

    def __init__(self, num_colors):
        self.num_colors = num_colors
        self.colors = {}

    def __setitem__(self, key, value):
        if key >= self.num_colors:
            raise ValueError(
                f"palette index {key} is greater than allowed by num_colors {self.num_colors}"
            )
        if not isinstance(value, (bytes, int)):
            raise ValueError(f"palette color should be bytes, not {type(value)}")
        if isinstance(value, int) and value > 255:
            raise ValueError(f"palette color int {value} is too large")
        if self.colors.get(key):
            raise ValueError(
                f"palette color {key} was already set, should not reassign"
            )
        self.colors[key] = value

    def __getitem__(self, item):
        if item >= self.num_colors:
            raise ValueError(
                f"palette index {item} should be less than {self.num_colors}"
            )
        if not self.colors.get(item):
            raise ValueError(f"palette index {item} is not set")
        return self.colors[item]

    def validate(self):
        if not self.colors:
            raise ValueError("no palette colors were set")
        if len(self.colors) > self.num_colors:
            raise ValueError("too many colors inserted into palette")
        for i in range(self.num_colors):
            try:
                self.colors
            except IndexError:
                raise ValueError("missing color `{}` in palette color list".format(i))

    def __str__(self):
        out = "\nPalette:\n"
        for y in range(len(self.colors)):
            out += f" [{y}] {self.colors[y]}\n"
        return out
