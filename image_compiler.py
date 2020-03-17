import os
import sys
import colorgram

import PIL
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
import numpy as np
import default_palettes
import image_formats

# Constants
if len(sys.argv) > 1:
    COLOR_BIT_LENGTH = int(sys.argv[1])
TRANSPARENCY = False

MAX_COLORS = 2**COLOR_BIT_LENGTH

def get_color_differance(c1, c2):
    # https://en.wikipedia.org/wiki/Color_difference
    r1, g1, b1, a1 = c1
    r2, g2, b2, a2 = c2
    return (r2-r1)**2 + (g2-g1)**2 + (b2-b1)**2 + (a2-a1)**2

def get_closest_color(color, color_palette):
    closest = color_palette[0]
    closest_distance = get_color_differance(color_palette[0], color)

    for c in color_palette[1:]:
        d = get_color_differance(c, color)
        if d < closest_distance:
            closest = c
            closest_distance = d

    return closest

def reduce_colors(img, color_palette):
    for x in range(img.width):
        for y in range(img.height):  
            original_color = img.getpixel((x,y))
            if len(original_color) == 3:
                original_color = original_color + (255,)
            img.putpixel( (x,y), get_closest_color(original_color, color_palette) )

def find_index(color, color_palette):
    for i in range(0, len(color_palette)):
        if color_palette[i] == color:
            return i
    raise Exception('color "{}" does not exist in the provided color_palette.'.format(color))
    
def image_to_pallete_indices(img, color_palette):
    indices = []
    for y in range(img.height):
        indices.append([])
        for x in range(img.width):  
            original_color = img.getpixel((x,y))
            if len(original_color) == 3:
                original_color = original_color + (255,)
            indices[y].append( find_index(original_color, color_palette) )
            img.putpixel( (x,y), get_closest_color(original_color, color_palette) )
    return indices

if len(sys.argv) < 3:
    print("No file argument found. Usage: image-compiler.py <filename>")
else:
    filename = sys.argv[2]
    if os.path.exists(filename):
        print("Compiling image: {}".format(os.path.basename(filename)))
        img = Image.open(filename)
        # Generate palette
        small_palette = colorgram.extract(img, MAX_COLORS-1 if TRANSPARENCY else MAX_COLORS)
        if TRANSPARENCY:
            small_palette = [(0,0,0,0)] + small_palette # Include full transparency in palette

        reduce_colors(img, small_palette)
        image_p = image_to_pallete_indices(img, small_palette)
        # Do someting with resulting image
        #print("\nVHDL IMAGE DATA")
        #print(image_formats.vhdl_style( image_p, COLOR_BIT_LENGTH ) )
        #print("VHDL COLOR PALETTE")
        #print(image_formats.vhdl_style_palette( small_palette ))
        print("PIXEL_BIT_SIZE:         {}".format(COLOR_BIT_LENGTH))
        print("PALETTE_PIXEL_BIT_SIZE: 32\n")
        print("IMAGE SIZE:   {}".format(COLOR_BIT_LENGTH*len(image_p[0])*len(image_p)))
        print("PALETTE SIZE: {}".format(32*len(small_palette)))
        print("TOTAL SIZE:   {}".format(len(image_p[0])*len(image_p)*COLOR_BIT_LENGTH + 32*len(small_palette)))
        if len(sys.argv) > 3:
            output_path = sys.argv[3]
            if os.path.exists(os.path.dirname(os.path.abspath(output_path))):
                img.save(output_path)
                print("Compilation complete, output saved as: {}".format(output_path))
            else:
                print("Invalid output file name, save folder not found")
    else:
        print("Invalid file name, file not found")

