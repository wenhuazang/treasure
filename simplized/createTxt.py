import os
from os import listdir


def create(folder, char_num, kinds, flag):
    char_num *= 4
    train_data_set = []
    val_data_set = []
    folder_name = listdir(folder)
    for folders in folder_name:
        if folders == '.DS_Store':
            continue
        file_name = listdir(folder + '/'+ folders)
        count = 0
        for files in file_name:
            if files == '.DS_Store':
                continue
            path_label = []
            path_label.extend(['/' + folders + '/' + files + ' ' + label_code(folders) + '\n'])

            if count < char_num / 6 * 5.0:
                train_data_set.extend(path_label)
                count += 1
            else:
                val_data_set.extend(path_label)

    store_set(train_data_set, 'train_' + str(kinds) + '_' + str(char_num) + '_' + flag + '.txt')
    store_set(val_data_set, 'val_' + str(kinds) + '_' + str(char_num) + '_' + flag + '.txt')


def label_code(folder_name):
    code = int(folder_name)
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


def store_set(input_set, file_name):
    fw = open(file_name, 'w')
    fw.writelines(input_set)
    fw.close()
