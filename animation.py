#!/usr/bin/python

#import pyglet, sys, os, time
import sys, os, time
from PIL import Image
from convert import render

def animgif_to_ASCII_animation(path):

    #anim = pyglet.image.load_animation(path)

    count = processImage(path)
    i = 0
    frames = ["" for x in range(count)]

    while i < count:
        frame = Image.open(str(i) + '.jpg')
        frames[i] = render(frame, 1)
        i += 1

    i = 0

    # Step through forever, frame by frame
    while True:
        os.system('clear')
        if (i == count):
            i = 0
        print frames[i]
        time.sleep(0.1)
        i += 1


def processImage(path):

    im = Image.open(path)
    i = 0
    mypalette = im.getpalette()

    try:
        while 1:
            im.putpalette(mypalette)
            new_im = Image.new("RGBA", im.size, (255, 255, 255))
            new_im.paste(im)

            pixel_data = new_im.load()
            if new_im.mode == "RGBA":
                for y in xrange(new_im.size[1]): # For each row ...
                    for x in xrange(new_im.size[0]): # Iterate through each column ...
                        if pixel_data[x, y][3] < 255:
                            pixel_data[x, y] = (255, 255, 255, 255)

            new_im.save(str(i) + '.jpg')

            i += 1
            im.seek(im.tell() + 1)

    except EOFError:
        pass

    return i


path = sys.argv[1]
animgif_to_ASCII_animation(path)
