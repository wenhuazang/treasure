# coding=utf-8
from PIL import Image
import os
from os import listdir
import random
from numpy import *
import createTxt
import create_single_char as csc
import deal_with_image as deal
import segment as seg

upperSize = (145, 40)
fontSet = ['simsun.ttc', 'hwzs.ttf']
fontSize = 25
bgColor = (255, 255, 255)
upperPart = Image.new('RGB', upperSize, bgColor)

fr = open('code.txt')
code = [inst.strip().split(' ')[1].decode('utf-8') for inst in fr.readlines()]


def createCharSet(kinds, charNum, folder):
    gap = 5
    start = 10
    letterarray = ['a', 'a', 'a', 'a']
    NumOfChar = 0
    charNum /= 4

    if not os.path.exists(folder):
        os.makedirs(folder)
    if kinds > 6763:
        kinds = 6763

    for i in range(kinds):

        letter = code[i]
        if letter == -1:
            break
        NumOfChar += 1

        for j in range(0, charNum):
            num = 4
            upperPart = Image.new('RGB', upperSize, bgColor)
            for k in range(0, num):

                fontIndex = random.randint(0, 2)
                imgchr = csc.creatChar(letter, fontSet[fontIndex], fontSize)
                letterarray[k] = letter
                imgchr = imgchr.convert("RGBA")

                imgchr = imgchr.rotate(random.randint(-10, 10), expand=0)
                r, g, b, a = imgchr.split()
                mask = a
                x = start + fontSize * k + random.randint(3, gap) + gap * k
                upperPart.paste(imgchr, (x, random.randint(0, 5)), mask)

            upperPart = upperPart.convert('L')
            if random.randint(1, 10) <= 8:
                upperPart = deal.draw_line(upperPart)

            # 分割并储存
            ###################
            seg.cut(upperPart, folder, NumOfChar, j)
            ###################
    createTxt.create(folder, charNum, kinds, 'c')


def createPinyinSet(kinds, charNum, folder):
    gap = 5
    start = 10
    letterarray = ['a', 'a', 'a', 'a']
    NumOfpinyin = 0
    charNum /= 4

    for i in range(kinds):

        letter = code[i + 6763]
        NumOfpinyin += 1

        for j in range(0, charNum):
            num = 4
            upperPart = Image.new('RGB', upperSize, bgColor)
            for k in range(0, num):

                fontIndex = 1
                imgchr = csc.creatPinyin(letter, fontSet[fontIndex], fontSize)
                letterarray[k] = letter

                imgchr = imgchr.convert("RGBA")
                imgchr = imgchr.rotate(random.randint(-10, 10), expand=0)
                r, g, b, a = imgchr.split()
                mask = a
                x = start + fontSize * k + random.randint(3, gap) + gap * k
                upperPart.paste(imgchr, (x, random.randint(0, 5)), mask)

            upperPart = upperPart.convert('L')
            if random.randint(1, 10) <= 8:
                upperPart = deal.draw_line(upperPart)

            # 分割并储存
            ###################
            seg.cut(upperPart, folder, NumOfpinyin, j)
            ###################

    # 对拼音文件编号
    FileList = listdir(folder)
    m = len(FileList)
    for i in range(m):
        fileNameStr = FileList[i]
        os.rename(folder + '/' + fileNameStr, folder + '/' + str(i + 6763))

    createTxt.create(folder, charNum, kinds, 'p')