#!coding=utf-8
import ImageFont, ImageDraw, ImageFilter, time
from PIL import Image
import os
from os import listdir
import pylab
from numpy import *

BACKGROUND = 255
NUM = 4


def findValley(w, y):
    valley = []
    num = [42, 71, 100]
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
    valley = valley + [13, 128]
    valley.sort()
    #print valley

    boxes = []
    arr = array(im)
    shadow = [0] * h

    for i in range(NUM):
        for k in range(valley[i]-1, valley[i + 1]):
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
        boxes.append([valley[i] + 1, start, valley[i + 1] - 1, start + 28])
        #print (boxes[i][2] - boxes[i][0])
    if not boxes:
        return None
    regions = []
    for box in boxes:
        regions.append(im.crop(box))
    return regions

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


def cut(image, folder, NumOfChar, j):
        regions = segment(image)
        a = 0
        for region in regions:
            if not os.path.exists(folder + '/' + str(NumOfChar - 1)):
                os.makedirs(folder + '/' + str(NumOfChar - 1))
            path = folder + '/' + str(NumOfChar - 1) + '/' + str(4*j+a) + '.png'
            region.save(path)
            a += 1