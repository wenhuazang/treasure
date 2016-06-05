#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5
import os
from os import listdir
from PIL import Image
import numpy as np
from numpy import *
import thread


class RClient(object):
    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


def getlabel1(files, stop_point, root1, root2, finished_thread):
    stop_point0 = stop_point
    flag = 0
    present = '-1'
    while not (present == files[-1] or present == files[-2]):
        for image_name in files:
            if image_name == '.DS_Store':
                continue
            if image_name.split('.')[0] == stop_point0:
                flag = 1
            if flag == 1:
                if int(image_name.split('.')[0]) % 2 == 1:
                    im = open(root1 + image_name, 'rb').read()
                    image = Image.open(root1 + image_name)
                    try:
                        label = rc.rk_create(im, 4010)['Result']
                        if not os.path.exists(root2 + label):
                            os.makedirs(root2 + label)
                        image.save(root2 + label + '/' + image_name)
                        print image_name.split('.')[0] + ':' + label
                        present = image_name
                    except:
                        print image_name.split('.')[0] + ':' + 'connection error!'
                        stop_point0 = image_name.split('.')[0]
                        flag = 0
                        break
    finished_thread[0] += 1


def getlabel2(files, stop_point, root1, root2, finished_thread):
    stop_point0 = stop_point
    flag = 0
    present = '-1'
    while not (present == files[-1] or present == files[-2]):
        for image_name in files:
            if image_name == '.DS_Store':
                continue
            if image_name.split('.')[0] == stop_point0:
                flag = 1
            if flag == 1:
                if int(image_name.split('.')[0]) % 2 == 0:
                    im = open(root1 + image_name, 'rb').read()
                    image = Image.open(root1 + image_name)
                    try:
                        label = rc.rk_create(im, 4010)['Result']
                        if not os.path.exists(root2 + label):
                            os.makedirs(root2 + label)
                        image.save(root2 + label + '/' + image_name)
                        print image_name.split('.')[0] + ':' + label
                        present = image_name
                    except:
                        print image_name.split('.')[0] + ':' + 'connection error!'
                        stop_point0 = image_name.split('.')[0]
                        flag = 0
                        break
    finished_thread[0] += 1


if __name__ == '__main__':
    rc = RClient('username', 'passwiord', '60913', 'e7d4651bbaf148f9b37f8b9307d820d9')
    root1 = 'Image/'
    root2 = 'DATA/'
    files = listdir(root1)
    m = len(files) / 2
    post_mode = 0  # 0是从头运行的模式;1是人为断点启动模式
    if post_mode == 0:
        stop_point1_1 = files[1].split('.')[0]
        stop_point1_2 = files[1].split('.')[0]
        stop_point2_1 = files[m].split('.')[0]
        stop_point2_2 = files[m].split('.')[0]
    else:
        stop_point1_1 = '12567'
        stop_point1_2 = '12568'
        stop_point2_1 = '12589'
        stop_point2_2 = '12590'
    finished_thread = [0]
    try:
        thread.start_new_thread(getlabel1, (files[:m], stop_point1_1, root1, root2, finished_thread))
        thread.start_new_thread(getlabel2, (files[:m], stop_point1_2, root1, root2, finished_thread))
        thread.start_new_thread(getlabel1, (files[m:], stop_point2_1, root1, root2, finished_thread))
        thread.start_new_thread(getlabel2, (files[m:], stop_point2_2, root1, root2, finished_thread))
    except:
        print "Error: unable to start thread"
    while finished_thread[0] < 4:
        pass
