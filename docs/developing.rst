"""""""""""""""""
Developing
"""""""""""""""""

Strategy:
* read headers to determine file type
* keep a pointer to the start of data
* read data into the Palette for all colors present
* rewind the file pointer back to start of data
* read data into the Bitmap
* return a bitmap and palette instance

Shared Bindings
===============

This library uses interfaces from CircuitPython's `displayio` module (Bitmap and Palette) to load images from disk into memory.

The Bitmap and Palette objects are related, and together can be used to display the image on a screen for the user.



The Palette is a list of colors present in the image.
Its constructor takes a single argument: (int) max_colors, representing how many colors will be populated in the palette.


====================
Palette code example
====================

.. code:: python

    palette = Palette(4)  # 4 represents that we will define four colors in palette
    palette[0] = b'\x00\x00\x00\x00'  # white
    palette[1] = b'\xFF\x00\x00\x00'  # red
    palette[2] = b'\x00\xFF\x00\x00'  # green
    palette[3] = b'\x00\x00\xFF\x00'  # blue


====================
Bitmap code example
====================

.. code:: python

    bitmap = Bitmap(3, 2, 4)  # 3 pixels wide, two pixels tall, 4 colors
    bitmap[0,0] = 0  # palette color 0
    bitmap[0,1] = 1  # palette color 1
    ...

============================
Example of Palette and Image
============================

The example is 4bit.bmp from the examples/images folder:

.. image:: ../examples/images/4bit.bmp
   :height: 17
   :width: 15
   :alt: 4bit image

The Palette object appears like this after loading::

    Palette:
    [0] b'\x00\x00\x00\x00'
    [1] b'\x7f\x00\x00\x00'
    [2] b'\xff\x00\x00\x00'
    [3] b'w\x00\xb1\x00'
    [4] b'\xff\x00\x9d\x00'
    [5] b'\x00\x00\xff\x00'
    [6] b'\xff\x00\xfe\x00'
    [7] b'\xbf\x80\x00\x00'
    [8] b'zzz\x00'
    [9] b'\xff\x9e\xa5\x00'
    [10] b'\x00\x98\xff\x00'
    [11] b'\x00\xff\x00\x00'
    [12] b'h\xff\x00\x00'
    [13] b'\xfb\xff\x9e\x00'
    [14] b'\x00\xfb\xff\x00'
    [15] b'\xfb\xfb\xfb\x00'

This palette has 16 colors. The value in square brackets [] is the color's index in the palette. The byte values are the RGB or RGB + padding of each color.

The Bitmap is an grid of which palette color to use in each position of the image.

The corresponding Bitmap to the example above appears like this after loading::

    5   5   5   5   5   5   5   5   5   5   5   5   5   5   5
    5   5   5   5   5   5   5   5   5   5   5   5   5   5   5
    5   5   5   5   5   5   5   5   5   5   5   5   5   5   5
    11  11  11   5   5   5  15  15  15   5   5   5   2   2   2
    11  11  11   5   5   5  15  15  15   5   5   5   2   2   2
    6   6   6   5   5   5   1   1   1   5   5   5  10  10  10
    6   6   6   5   5   5   1   1   1   5   5   5  10  10  10
    6   6   6   5   5   5   1   1   1   5   5   5  10  10  10
    14  14  14   5   5   5   9   9   9   5   5   5   8   8   8
    14  14  14   5   5   5   9   9   9   5   5   5   8   8   8
    14  14  14   5   5   5   9   9   9   5   5   5   8   8   8
    3   3   3   5   5   5   0   0   0   5   5   5  13  13  13
    3   3   3   5   5   5   0   0   0   5   5   5  13  13  13
    4   4   4   5   5   5  12  12  12   5   5   5   7   7   7
    4   4   4   5   5   5  12  12  12   5   5   5   7   7   7
    4   4   4   5   5   5  12  12  12   5   5   5   7   7   7
    5   5   5   5   5   5   5   5   5   5   5   5   5   5   5

This grid represents the example image (``15 pixels wide`` and  ``17 pixels tall``).
The coordinates are arranged in a zero indexed grid, starting in the top left at ``[0,0]``,
and continuing down and to the right to a final coordinate of ``[14,16]``.


The value at each position is an integer, representing an entry in the palette object.



For example, the Bitmap coordinate ``[0,0]`` has the value (integer) ``5``.


This corresponds to the the Palette object's, ``[5]`` which is ``b'\x00\x00\xff\x00'``. This is a byte string that represents a color.
