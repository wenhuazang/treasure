# -*- coding: utf-8 -*-
import os
from os import listdir
from PIL import Image
import random
from numpy import *
from pypinyin import pinyin, lazy_pinyin
from PIL import Image, ImageDraw, ImageFont
import createTxt

class Create:
    def __init__(self):
        self.upperSize = (145, 40)
        self.fontSet = ['simsun.ttc', 'hwzs.ttf']
        self.fontSize = 23
        self.bgColor = (255, 255, 255)
        self.upperPart = Image.new('RGB', self.upperSize, self.bgColor)
        self.imageChar = ImageChar()

        ###################
        self.head = 0xB0
        self.body = 0x9
        self.tail = 0xF
        ###################
        fr = open('code.txt')
        self.code = [inst.strip().split(' ')[1].decode('utf-8') for inst in fr.readlines()]

    def creatCharSet(self, kinds, charNum, folder):
        gap = 5
        start = 10
        letterarray = ['a', 'a', 'a', 'a']
        NumOfChar = 0
        charNum = charNum / 4

        if not os.path.exists(folder):
            os.makedirs(folder)

        for i in range(kinds):

            letter = self.code[i]
            if letter == -1:
                break
            NumOfChar += 1

            for j in range(0, charNum):
                num = 4
                self.upperPart = Image.new('RGB', self.upperSize, self.bgColor)
                for k in range(0, num):

                    fontIndex = random.randint(0, 1)

                    imgchr = self.imageChar.creatChar(letter, self.fontSet[fontIndex], self.fontSize)
                    char = self.imageChar.getChar()
                    letterarray[k] = char
                    if not os.path.exists(folder + '/' + str(NumOfChar - 1)):
                        os.makedirs(folder + '/' + str(NumOfChar - 1))

                    imgchr = imgchr.convert("RGBA")

                    imgchr = imgchr.rotate(random.randint(-10, 10), expand=0)
                    r, g, b, a = imgchr.split()
                    mask = a
                    x = start + self.fontSize * k + random.randint(3, gap) + gap * k
                    self.upperPart.paste(imgchr, (x, random.randint(0, 5)), mask)

                self.upperPart = self.upperPart.convert('L')
                if random.randint(1, 10) <= 8:
                    self.upperPart = self.drawLine(self.upperPart)

                # 分割并储存
                ###################
                image = array(self.upperPart)
                for m in range(0, num):
                    eachchar = Image.new('L', (35, 40), 255)
                    temp = array(eachchar)
                    for x in range(7, 35):
                        for y in range(40):
                            temp[y, x - 3] = image[y, x - 7 + 28 * m + 13]
                    eachchar = Image.fromarray(temp)
                    path = folder + '/' + str(NumOfChar - 1) + '/' + str(j) + str(m) + '.png'
                    self.save(eachchar, path)
                    ###################
        createTxt.create(folder, charNum, kinds, 'c')

    def creatPinyinSet(self, kinds, charNum, folder):
        gap = 5
        start = 10
        letterarray = ['a', 'a', 'a', 'a']
        NumOfpinyin = 0
        charNum = charNum / 4

        for i in range(kinds):

            letter = self.code[i + 6763]
            NumOfpinyin += 1

            for j in range(0, charNum):
                num = 4
                self.upperPart = Image.new('RGB', self.upperSize, self.bgColor)
                # pinyinIndex=random.randint(0, 3)
                for k in range(0, num):

                    fontIndex = random.randint(0, 1)

                    # if k==pinyinIndex:
                    imgchr = self.imageChar.creatPinyin(letter, self.fontSet[fontIndex], self.fontSize)
                    char = self.imageChar.getChar()
                    letterarray[k] = char
                    if not os.path.exists(folder + '/' + char.encode('utf-8')):
                        os.makedirs(folder + '/' + char.encode('utf-8'))
                    # else:
                    #    imgchr = self.imageChar.creatChar(letter,self.fontSet[fontIndex],self.fontSize)

                    imgchr = imgchr.convert("RGBA")
                    imgchr = imgchr.rotate(random.randint(-10, 10), expand=0)
                    r, g, b, a = imgchr.split()
                    mask = a
                    x = start + self.fontSize * k + random.randint(3, gap) + gap * k
                    self.upperPart.paste(imgchr, (x, random.randint(0, 5)), mask)

                self.upperPart = self.upperPart.convert('L')
                if random.randint(1, 10) <= 8:
                    self.upperPart = self.drawLine(self.upperPart)

                # 分割并储存
                ###################
                image = array(self.upperPart)
                for m in range(0, num):
                    eachchar = Image.new('L', (35, 40), 255)
                    temp = array(eachchar)
                    for x in range(7, 35):
                        for y in range(40):
                            temp[y, x - 3] = image[y, x - 7 + 28 * m + 13]
                    eachchar = Image.fromarray(temp)
                    path = folder + '/' + letterarray[m].encode('utf-8') + '/' + str(j) + str(m) + '.png'
                    self.save(eachchar, path)
                    ###################

        # 对拼音文件编号
        FileList = listdir(folder)
        m = len(FileList)
        for i in range(m):
            fileNameStr = FileList[i]
            os.rename(folder + '/' + fileNameStr, folder + '/' + str(i + 6763))

        createTxt.create(folder, charNum, kinds, 'p')

    def getGB2312(self):

        while 1:
            self.tail = self.tail + 1
            if self.tail > 0xF:
                self.tail = 0
                self.body = self.body + 1
            if self.body > 0xF:
                self.body = 0xA
                self.head = self.head + 1
            if self.head > 0xF7:
                exit(0)
            if not ((self.body == 0xF) and (self.tail == 0xF)):
                if not ((self.body == 0xA) and (self.tail == 0x0)):
                    if not ((self.head == 0xD7) and (self.body == 0xF) and (self.tail > 0x9)):
                        break

        # save head,body,tail
        ###################


        ###################

        val = (self.head << 8) | (self.body << 4) | self.tail
        # print val
        str = "%x" % val
        # print str ###
        char = str.decode('hex').decode('gb2312')
        # print char ###
        return char

    def drawLine(self, Im):
        image = array(Im)
        para0 = random.random() * 3
        para1 = random.random() * 19 + 2
        for y in range(145):
            x = round(18 * abs(sin(para0 / 145 * (y + 1))) + para1)
            image[x, y] = 0
            image[x - 1, y] = 0
        im = Image.fromarray(image)
        return im

    def save(self, img, path):
        img.save(path)


class ImageChar:
        def __init__(self, fontColor=(0, 0, 0),
                     size=(50, 50),
                     fontPath='simsun.ttc',
                     bgColor=(255, 255, 255),
                     fontSize=23):
            self.size = size
            self.fontPath = fontPath
            self.bgColor = bgColor
            self.fontSize = fontSize
            self.fontColor = fontColor
            self.font = ImageFont.truetype(self.fontPath, self.fontSize)
            self.pos = (2, 2)
            self.image = Image.new('RGB', size, bgColor)
            self.char = '啊'

        def setFont(self, path, fontSize):
            self.fontPath = path
            self.fontSize = fontSize
            self.font = ImageFont.truetype(path, fontSize)

        def drawText(self, pos, txt, fill):
            draw = ImageDraw.Draw(self.image)
            draw.text(pos, txt, font=self.font, fill=fill)

        def creatPinyin(self, pinyin, fontPath, fontSize):
            temp = fontSize
            self.image = Image.new('RGB', self.size, self.bgColor)
            self.char = pinyin
            a = lazy_pinyin(self.char)
            self.char = str(a[0])
            if len(self.char) < 3:
                pass
            elif len(self.char) == 3:
                temp -= 7
            elif len(self.char) == 4:
                temp -= 10
            elif len(self.char) == 5:
                temp -= 13
            elif len(self.char) >= 6:
                temp -= 16
            self.setFont(fontPath, temp)
            self.drawText(self.pos, self.char, self.fontColor)
            # print self.char
            return self.image

        def creatChar(self, char, fontPath, fontSize):
            self.setFont(fontPath, fontSize)
            self.image = Image.new('RGB', self.size, self.bgColor)
            self.char = char
            # print self.char ###
            self.drawText(self.pos, self.char, self.fontColor)
            return self.image

        def getChar(self):
            return self.char

        def save(self, img, path):
            img.save(path)