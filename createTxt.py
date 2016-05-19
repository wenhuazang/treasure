import os
from os import listdir

def create(folder, charNum, kinds, flag):
    charNum = charNum * 4
    trainDataSet = []
    valDataSet = []
    foldername = listdir(folder)
    for folders in foldername:
        if folders == '.DS_Store':
            continue
        filename = listdir(folder + '/'+ folders)
        n = len(filename)
        for filenum in range(int(charNum/6*5.0)):
            if filename[filenum] == '.DS_Store':
                continue
            Path_Label=[]
            Path_Label.extend(['/' + folders + '/' + filename[filenum] + ' ' + labelcode(folders) + '\n'])
            trainDataSet.extend(Path_Label)

        for filenum in range(int(charNum/6*5.0),charNum):
            if filename[filenum] == '.DS_Store':
                continue
            Path_Label = []
            Path_Label.extend(['/' + folders + '/' + filename[filenum] + ' ' + labelcode(folders) + '\n'])
            valDataSet.extend(Path_Label)

    storeSet(trainDataSet,'train_' + str(kinds) + '_' + str(charNum) + '_' + flag + '.txt')
    storeSet(valDataSet,'train_' + str(kinds) + '_' + str(charNum) + '_' + flag + '.txt')


def labelcode(foldername):
    code = int(foldername)
    if code < 10:
        name = '000' + str(code)
        return name
    elif code < 100:
        name = '00' + str(code)
        return name
    elif code < 1000:
        name = '0' + str(code)
        return name
    elif code < 10000:
        return str(code)


def storeSet(inputSet,filename):
    fw = open(filename,'w')
    fw.writelines(inputSet)
    fw.close()
