Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-imageload/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/imageload/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad/actions/
    :alt: Build Status

This library decodes an image file into new bitmap and palette objects of the provided type. It's
designed to load code needed during decoding as needed. This is meant to minimize the memory
overhead of the decoding code.

Only certain types of bitmaps work with this library, and they often have to be exported in specific ways. To find out what types are supported and how to make them, see `this learn guide page.
<https://learn.adafruit.com/creating-your-first-tilemap-game-with-circuitpython/indexed-bmp-graphics>`_

Usage Example
=============

.. code-block:: python

    import board
    import displayio
    import adafruit_imageload

    image, palette = adafruit_imageload.load(
        "images/4bit.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
    )
    tile_grid = displayio.TileGrid(image, pixel_shader=palette)

    group = displayio.Group()
    group.append(tile_grid)
    board.DISPLAY.show(group)

    while True:
        pass


Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/imageload/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
