import logging



def load(f, magic_number, header, bitmap = None , palette = None):
    # type: (stream, str, list, c_obj, c_obj) -> bitmap, palette
    """
    Load a P1 or P4 Netpbm 'PBM' image into bitmap
    """
    width = header[0]
    height = header[1]

    logging.info(f'height: {height} width {width}')
    if palette:
        palette = palette(1)
    if bitmap:
        bitmap = bitmap(width, height, 1)
        if magic_number == b'P1':  # ASCII space packed file
            next_byte = True
            for line in range(height):
                col = 1
                while next_byte:
                    next_byte = f.read(1)
                    if not next_byte.isdigit():
                        continue
                    bitmap[line] = next_byte
                    if col == width:
                        break
                    col += 1
            return bitmap, palette
        if magic_number == b'P4':  # binary read from file as hex

            min_read = width // 8
            dirty_bits = bytes()
            chunk = bytearray(width)
            for line in range(height):
                data = dirty_bits + f.read(min_read if dirty_bits else min_read + 1)
                row = data[:width]
                dirty_bits = data[width:]
                for i in range(8):
                    byte = access_bit(row, i)
                #    data.readinto(1)
                    logging.info(f'row {row} byte {byte} {type(row)}')
                    bitmap[line] = byte
            return bitmap, palette
        raise NotImplementedError('magic number {}'.format(magic_number))


def access_bit(data, num):
    base = int(num/8)
    shift = num % 8
    return (data[base] & (1<<shift)) >> shift