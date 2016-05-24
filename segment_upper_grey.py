#!coding=utf-8
import ImageFont, ImageDraw, ImageFilter, time
from PIL import Image
import os
import pylab
from numpy import *

BACKGROUND = 255
NUM = 4
adds = 60

def findValley(w, y):
    valley = []
    num = [37 + adds, 58 + adds, 80 + adds]
    for x in range(len(num)):
        for i in range(num[x] - 2, num[x] + 3):
            if y[i + 1] >= y[i] and y[i - 1] >= y[i]:
                valley.append(i + 1)
                break
        if len(valley) != x + 1:
            valley.append(num[x])
    return valley

def segment(im):
    y = []
    frame = im.load()
    (w, h) = im.size
    for i in range(w):
        a = 0
        for j in range(h):
            a += (255 - frame[i, j])
        y.append(a)
    valley = findValley(w,y)
    valley = valley + [13 + adds, 102 + adds]
    valley.sort()
    #print valley

    boxes = []
    arr = array(im)
    shadow = [0] * h

    for i in range(NUM):
        for k in range(valley[i]-1,valley[i + 1]+1):
            for j in range(h):
                if not (arr[j, k] == 255):
                    shadow[j] += 1
        start = 0
        sum = 0
        for k in range(h-27):
            temp_sum = 0
            for j in range(28):
                temp_sum += shadow[k+j]
            if temp_sum > sum:
                sum = temp_sum
                start = k
        if start < 0:
            start = 0
        boxes.append([valley[i] - 1, start, valley[i + 1] + 1, start + 28])
        #print (boxes[i][2] - boxes[i][0])
    if not boxes:
        return None
    regions = []
    for box in boxes:
        regions.append(im.crop(box))
    return regions


def getframe(fname):
    try:
        im = Image.open(fname,'r')
    except:
        return "File error!"
    im = im.convert('L')
    return im

def plot(img):
    img = img.convert('L')
    w,h = img.size
    d = img.load()
    x = []
    y = []
    for i in range(w):
        a = 0
        for j in range(h):
            a += (255 - d[i, j])
        y.append(a)
        x.append(i)
    pylab.plot(x, y)
    pylab.show()


if __name__ == "__main__":
    start = time.time()
    img_root = "TiebaChinese/"
    img_save = "results/"
    if not os.path.exists(img_save):
        os.makedirs(img_save)
    images = os.listdir(img_root)
    i = -1
    print "load samples..."
    for name in images:
        if name == '.DS_Store':
            continue
        a = 0
        i += 1
        img = getframe(img_root + name)
        regions = segment(img)
        if not len(name.split('.')[0].decode('utf-8')) == 4:
            sys.exit()
        for region in regions:
            if not os.path.exists(img_save + name.split('.')[0].decode('utf-8')[a]):
                os.makedirs(img_save + name.split('.')[0].decode('utf-8')[a])
            region.save(img_save + name.split('.')[0].decode('utf-8')[a] + '/' + str(4*i+a) +".png")
            a += 1
    end = time.time()
    print "elapse: %f" % (end - start)