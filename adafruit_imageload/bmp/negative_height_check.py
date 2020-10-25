"""
Check for negative height on the BMP.
Seperated into it's own file to support builds
without longint.
"""


def negative_height_check(height):
    """Check the height return modified if negative."""
    if height > 0x7FFFFFFF:
        return height - 4294967296
    return height
