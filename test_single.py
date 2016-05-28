# coding=utf-8
import caffe
import os
import numpy as np
import time


model_file = '/Users/zhangmingjie/Documents/caffe/examples/mnist/lenet.prototxt'
pretrained_file = '/Users/zhangmingjie/Documents/caffe/examples/mnist/lenet1/_iter_30000.caffemodel'
net = caffe.Classifier(model_file, pretrained_file, image_dims=(28, 28), raw_scale=255)


if __name__ == '__main__':
    start = time.time()

    predict_labels_path = '/Users/zhangmingjie/PycharmProjects/chameleon/134.png'

    print 'loading data...'

    #####################################################################
    image = predict_labels_path
    score = net.predict([caffe.io.load_image(image, color=False)], oversample=False)
    max_num = max(score[0])
    print score[0]
    for j in range(20):
        if score[0][j] == max_num:
             get = j
             break
    print 'This char is '+ ': ' + str(get)

    #####################################################################
