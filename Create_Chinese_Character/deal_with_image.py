from numpy import *
import random
from PIL import Image


def draw_line(Im):
    image = array(Im)
    para0 = random.random() * 3
    para1 = random.random() * 19 + 2
    for y in range(145):
        x = round(18 * abs(sin(para0 / 145 * (y + 1))) + para1)
        image[x, y] = 0
        image[x - 1, y] = 0
    im = Image.fromarray(image)
    return im
