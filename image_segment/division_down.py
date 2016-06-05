#!coding=utf-8
import os, time
from PIL import Image
import pylab

BACKGROUND = 255
save_single_part = "down_segment/"
root = "down_part/"
save_path = "horizon/"
NUM = 3
A = 200
except_width = []


def judge_point(inter_point, name):
    if len(inter_point) != 6:
        for i in range(len(inter_point) - 1):
            if inter_point[i + 1] - inter_point[i] > 36:
                # print(inter_point[i])
                inter_point.append((inter_point[i] + 23))
                inter_point.sort()
        # print "the len is: ",len(inter_point)
        # print "inter_point: ",inter_point
        print "add point name: ", name
        judge_point(inter_point, name)


def plot(img, name):
    img = img.convert('L')
    w, h = img.size
    d = img.load()
    x = []
    y = []
    for i in range(w):
        a = 0
        for j in range(h):
            a += (255 - d[i, j])
        y.append(a)
        x.append(i)
    y2 = []
    for i in range(len(x)):
        y2.append(A)
    pylab.plot(x, y, "o-", label="project_to_X")
    pylab.plot(x, y2, "r-", label="Y=200")
    pylab.legend()
    pylab.title(name)
    # pylab.save(str(m)+".jpg")
    pylab.show()


def findValley(w, y):
    valley = []
    num = [37, 58, 80]
    for x in range(len(num)):
        for i in range(num[x] - 2, num[x] + 3):
            if (y[i + 1] >= y[i] and y[i - 1] >= y[i]):
                valley.append(i + 1)
                break
        if (len(valley) != x + 1):
            valley.append(num[x])
    return valley


def findSolution():
    print "hehe"


def segment_column(region, count, name):
    x_y = {}
    frame = region.load()
    (w, h) = region.size
    for x in range(w):
        y = 0
        for j in range(h):
            y += (255 - frame[x, j])
        x_y.setdefault(x, y)

    X = []
    for i in range(w):
        if (x_y[i] >= A):
            X.append(i)
    # print X

    ################################
    # find the interrupt point
    ################################
    inter_point = []
    # print "len of X:",len(X)
    i = 12
    while i < len(X) - 10:
        if (X[i + 1] - X[i] > 8) and (X[i] != X[i + 1] - 1):
            # print i
            inter_point.append(X[i] + 4)
            inter_point.append(X[i + 1] - 4)
            i += 14  # ignore some point,so process some pixel
        else:
            i += 1

    inter_point.append(0)
    inter_point.append(119)
    inter_point.sort()
    # judge the number of segment point
    # recursion
    '''
    print "inter_point: ",inter_point
    print "name: ",name
    '''
    # print "project:　",X
    judge_point(inter_point, name)

    for i in range(len(inter_point) - 1):
        if (inter_point[i + 1] - inter_point[i] > 35):
            # print "the width too long name: ",name
            except_width.append(name)
    # print inter_point
    # print "project:　",X
    '''
    if (len(inter_point) != 6):
        print "name: ",name
        print "project:　",X
        print "inter_point: ",inter_point
        for i in range(len(inter_point) - 1):
            if (inter_point[i+1] - inter_point[i] > 50):
                print(inter_point[i])
                inter_point.append((inter_point[i] + 23))
                inter_point.sort()
    '''
    # print inter_point
    boxs = []
    i = 0
    while i < NUM * 2:
        boxs.append([inter_point[i], 0, inter_point[i + 1], 28])
        i += 2
    # boxs = [[0, 0, 24, 28],[51, 0, 76, 28],[95, 0, 120, 28]]
    # boxs = [[95, 0, 120, 28]]
    for box in boxs:
        new_region = region.crop(box)
        # new_region = tmp_region.crop(getbox(tmp_region))
        # print name
        # new_region.show()
        new_region.convert('L')
        new_region.save(save_single_part + str(count) + ".png")
        count += 1


def getframe(fname):
    try:
        im = Image.open(fname)
    except:
        return "File error!"
    im = im.convert("L")
    return im


if __name__ == "__main__":
    start = time.time()
    if not os.path.exists(save_single_part):
        os.mkdir(save_single_part)
    images = os.listdir(root)
    boxs = [[15, 6, 135, 34], [15, 54, 135, 82], [15, 104, 135, 132]]
    # boxs = [[15, 6, 135, 34]]
    count = 0
    # a = 0
    for name in images:
        if name == '.DS_Store':
            continue
        # print "segment image:",name
        for box in boxs:
            img = getframe(root + name)
            # print "name:" , a

            # segment according to raw first
            try:
                region = img.crop(box)
            except:
                print "the image is except: ", name
                pass
            # region.show()
            # region.save(save_path+str(a)+".jpg")
            segment_column(region, count, name)
            # a += 1
            count += 3
            # plot(region,name)
            # break
            # break
    print set(except_width)
    end = time.time()
    print "elapse :", (end - start)