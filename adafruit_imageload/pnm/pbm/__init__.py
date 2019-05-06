import logging



def load(f, magic_number, header, bitmap = None , palette = None):
    # type: (stream, str, list, c_obj, c_obj) -> bitmap, palette
    height = header[0]
    width = header[1]
    logging.info(f'height: {height}')
    if palette:
        palette = palette(1)
    if bitmap:
        bitmap = bitmap(header[0], header[1], 1)
        for line in range(height-1,-1,-1):

            chunk = f.read(width)
            #logging.info(chunk)
    return bitmap, palette

    #while not has 3 signnif