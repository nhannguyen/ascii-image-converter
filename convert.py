#!/usr/bin/python

import sys
import math
from PIL import Image


def getYIQ(r, g, b):
    return ((r * 0.299) + (g * 0.587) + (b * 0.114))

def findChar(sample, sample_mean, mean, sigma):
    if sample == '1111':
        if (sample_mean < mean - sigma) | (sample_mean < 0):
            return '@'
        elif sample_mean < mean - 0.3 * sigma:
            return 'O'
        elif sample_mean < mean:
            return 'o'
    elif sample == '0000':
        if (sample_mean > mean + sigma) | (sample_mean > 255):
            return ' '
        elif sample_mean > mean + 0.3 * sigma:
            return '.'
        elif sample_mean > mean:
            return '*'
    elif (sample == '1000') | (sample == '0010'):
        return '`'
    elif (sample == '0100') | (sample == '0001'):
        return ','
    elif sample == '1010':
        return '^'
    elif sample == '1100':
        return '['
    elif sample == '0011':
        return ']'
    elif sample == '0101':
        return '='
    elif (sample == '1001') | (sample == '1011') | (sample == '1101'):
        return '\\'
    elif (sample == '0110') | (sample == '0111') | (sample == '1110'):
        return '/'

def render(image, quality):
    result = ''
    width = image.size[0]
    height = image.size[1]

    s = 0
    count = 0
    yiqs = []

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            offset = y * width + x
            yiqs.append(getYIQ(r, g, b))
            s += yiqs[offset]
            count +=1

    mean = s / count
    sigma = 0
    for yiq in yiqs:
        sigma += (yiq - mean) * (yiq - mean)
    sigma = math.sqrt(sigma / count)

    for y in range(0, height - 2, quality * 2):
        for x in range(0, width - 2, quality):
            sample = ''
            sample_mean = 0

            i = y
            while i < y + 2:
                j = x
                while j < x + 2:
                    r, g, b = image.getpixel((j, i))
                    yyy = yiqs[i * width + j]
                    if yyy < mean:
                        sample += '1'
                    else:
                        sample += '0'
                    sample_mean += yyy
                    j += 1
                i += 1

            sample_mean /= 4
            result += findChar(sample, sample_mean, mean, sigma)
        result += '\n'
    return result


if (len(sys.argv) != 2) & (len(sys.argv) != 3):
    print("The corrent format is: python convert.py <path/to/image> [quality]")
else:
    quality = 3
    if len(sys.argv) == 3:
        quality = int(sys.argv[2])
    path = sys.argv[1]
    image = Image.open(path)
    result = render(image, quality)
    print result
