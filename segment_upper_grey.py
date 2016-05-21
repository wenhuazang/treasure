#!coding=utf-8
import Image, ImageFont, ImageDraw, ImageFilter, time
import os
import pylab

BACKGROUND = 255
NUM = 4

def findValley(w, y):
    valley = []
    num = [37,58,80]
    for x in range(len(num)):
        for i in range(num[x] - 2, num[x] + 3):
            if (y[i + 1] >= y[i] and y[i - 1] >= y[i]):
                valley.append(i + 1)
                break
        if (len(valley) != x+1):
            valley.append(num[x])
    return valley

def segment(im):
    y = []
    frame = im.load()
    (w, h) = im.size
    for i in range(w):
        a = 0
        for j in range(h):
            a += (255 - frame[i,j])
        y.append(a)
    valley = findValley(w,y)
    valley = valley+[13,102]
    valley.sort()
    print valley

    boxes = []
    for i in range(NUM):
        boxes.append([valley[i]-1,6,valley[i+1]+1,34])
        print (boxes[i][2] - boxes[i][0])
    if boxes == []:
        return None
    regions = []
    for box in boxes:
        regions.append(im.crop(box))
    return regions


def getframe(fname, strict=1):
    try:
        im = Image.open(fname)
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
            a += (255 - d[i,j])
        y.append(a)
        x.append(i)
    pylab.plot(x,y)
    pylab.show()


if __name__ == "__main__":
    start = time.time()
    img_root = "upper_part_samples/"
    img_save = "upper_segment/"
    images = os.listdir(img_root)
    i = -1
    print "load samples..."
    for name in images:
        a = 0
        i += 1
        img = getframe(img_root + name)
        regions = segment(img)
        for region in regions:
            region.save(img_save+str(4*i+a)+".jpg")
            a += 1
    end = time.time()
    print "elapse: %f" % (end - start)