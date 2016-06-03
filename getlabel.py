#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5
import os
from os import listdir
from PIL import Image
import numpy as np
from numpy import *

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


if __name__ == '__main__':
    rc = RClient('username', 'password', '60913', 'e7d4651bbaf148f9b37f8b9307d820d9')
    files = listdir('Image/')
    for image_name in files:
        if image_name == '.DS_Store':
            continue
        im = open('Image/' + image_name, 'rb').read()
        image = Image.open('Image/' + image_name)
        label = rc.rk_create(im, 4010)['Result']
        print label
        Im = array(image)
        mean = np.mean(Im)
        column, row = image.size
        for a in range(row):
            for b in range(column):
                if Im[a, b] < (mean - 33):
                    Im[a, b] = 0
                else:
                    Im[a, b] = 255
        for a in range(35):
            for b in range(40):
                pass
        image = Image.fromarray(Im)
        if not os.path.exists('DATA/'+ label):
            os.makedirs('DATA/'+ label)
        image.save('DATA/'+ label + '/' + image_name)

