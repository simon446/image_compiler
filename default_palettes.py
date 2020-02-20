def get_8bit_palette():
    return [(i & 0xE0, i & 0x1C, i & 0x03, 255) for i in range(0, 2**8)]
    
