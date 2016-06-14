# coding=utf-8
from PIL import Image,ImageFont,ImageDraw
from pypinyin import lazy_pinyin

fontColor = (0, 0, 0)
size = (50, 50)
bgColor = (255, 255, 255)
pos = (2, 2)
char = '啊'


def drawText(pos, txt, fill,image, font):
    draw = ImageDraw.Draw(image)
    draw.text(pos, txt, font=font, fill=fill)
    return image

def creatPinyin(pinyin, fontPath, fontSize):
    temp = fontSize
    image = Image.new('RGB', size, bgColor)
    char = pinyin
    a = lazy_pinyin(char)
    char = str(a[0])
    if len(char) < 3:
        pass
    elif len(char) == 3:
        temp -= 7
    elif len(char) == 4:
        temp -= 10
    elif len(char) == 5:
        temp -= 13
    elif len(char) >= 6:
        temp -= 16
    font = ImageFont.truetype(fontPath, fontSize)
    drawText(pos, char, fontColor, image, font)
    return image


def creatChar(char, fontPath, fontSize):
    font = ImageFont.truetype(fontPath, fontSize)
    image = Image.new('RGB', size, bgColor)
    image = drawText(pos, char, fontColor, image, font)
    return image
