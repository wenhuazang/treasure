# coding=utf-8
import sys
sys.path.append('/Users/zhangmingjie/Documents/caffe/python')
import caffe
import os
import numpy as np
import time


model_file = '/Users/zhangmingjie/Documents/caffe/examples/mnist/lenet.prototxt'
pretrained_file = '/Users/zhangmingjie/Documents/caffe/examples/mnist/lenet1/_iter_30000.caffemodel'
net = caffe.Classifier(model_file, pretrained_file, image_dims=(28, 28), raw_scale=255)


if __name__ == '__main__':
    start = time.time()
    # In this method, you have to put those image you want to make predictions about into folders, names of which are the labels those images belong to.   
    predict_labels_path = '/Users/zhangmingjie/Documents/Github/treasure/simplized/DATA/'
    
    print 'loading data...'

    #####################################################################
    folder = os.listdir(predict_labels_path)

    for i in range(len(folder)):
        files = os.listdir(predict_labels_path+str(i)+'/')
        count = 0
        get = -1
        num = 1
        for k in range((len(files)-1)/num):
             get = -1
             if (files[k] == '.DS_Store'):
                 continue
             image = predict_labels_path + str(i) + '/' + files[k]
             score = net.predict([caffe.io.load_image(image, color=False)], oversample=False)
             max_num = max(score[0])

             for j in range(len(folder)):
                 if score[0][j] == max_num:
                      get = j
                      break
             if get == i:
                 count += 1

        print count
        accuracy = 1.0 * count / ((len(files)-1)/num)
        print str(i) + ':' + str(accuracy)
  
    #####################################################################
