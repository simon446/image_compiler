
# Style image to fit in vhdl code
#
# x"FF",x"FF",x"00",x"00",x"00",x"FF",x"FF",x"FF",
# x"FF",x"00",x"00",x"FF",x"00",x"00",x"FF",x"FF",
# x"00",x"00",x"FF",x"FF",x"FF",x"00",x"00",x"FF",
# x"00",x"00",x"FF",x"FF",x"FF",x"00",x"00",x"FF",
# x"00",x"00",x"00",x"00",x"00",x"00",x"00",x"FF",
# x"00",x"00",x"FF",x"FF",x"FF",x"00",x"00",x"FF",
# x"00",x"00",x"FF",x"FF",x"FF",x"00",x"00",x"FF",
# x"FF",x"FF",x"FF",x"FF",x"FF",x"FF",x"FF",x"FF",
def vhdl_style(image_p, bits):
    string = ""
    for y in range(0, len(image_p)):
        for x in range(0, len(image_p[y])):
            if bits % 4 == 0:
                string = string + ("x\"{0:0"+str(int(bits/4))+"x}\",").format(image_p[y][x])
            else:
                string = string + ("\"{0:0"+str(int(bits))+"b}\",").format(image_p[y][x])

        string = string + '\n'
    return string

def vhdl_style_palette(color_palette):
    string = ""
    for c in color_palette:
        string = string + 'x"{}",'.format(color_to_24_bit_string(c))
        string = string + '\n'
    return string

def color_to_24_bit_string(color):
    return '{0:08x}'.format(color[0] << 24 | color[1] << 16 | color[2] << 8 | color[3])