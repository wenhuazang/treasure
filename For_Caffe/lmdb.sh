# 将图片批量生成lmbd格式的数据存储

#----------------------------------------------------------------------------------------- 

#保存生成的lmdb的目录
EXAMPLE=/Users/zhangmingjie/Documents/lmdb/lmdb1/

#train.txt和val.txt所在的目录
DATA=/Users/zhangmingjie/Documents/Github/treasure/simplized/

#转换图片的工具所在的目录
TOOLS=/Users/zhangmingjie/Documents/caffe/build/tools


#图片所在的目录
TRAIN_DATA_ROOT=/Users/zhangmingjie/Documents/Github/treasure/simplized/DATA/

VAL_DATA_ROOT=/Users/zhangmingjie/Documents/Github/treasure/simplized/DATA/

# 设置 RESIZE=true 可以把图片resize成想要的尺寸。
RESIZE=true
if $RESIZE; then
 RESIZE_HEIGHT=28
 RESIZE_WIDTH=28
else
 RESIZE_HEIGHT=0
 RESIZE_WIDTH=0
fi


if [ ! -d "$TRAIN_DATA_ROOT" ]; then
 echo "Error: TRAIN_DATA_ROOT is not a path to a directory: $TRAIN_DATA_ROOT"
 echo "Set the TRAIN_DATA_ROOT variable in create_imagenet.sh to the path" \
      "where the ImageNet training data is stored."
 exit 1
fi


if [ ! -d "$VAL_DATA_ROOT" ]; then
 echo "Error: VAL_DATA_ROOT is not a path to a directory: $VAL_DATA_ROOT"
 echo "Set the VAL_DATA_ROOT variable in create_imagenet.sh to the path" \
      "where the ImageNet validation data is stored."
 exit 1
fi


echo "Creating train lmdb..."


GLOG_logtostderr=1 $TOOLS/convert_imageset \
  --resize_height=$RESIZE_HEIGHT \
  --resize_width=$RESIZE_WIDTH \
  --shuffle \
  --gray \
  $TRAIN_DATA_ROOT \
  $DATA/train.txt \
  $EXAMPLE/train_lmdb


echo "Creating val lmdb..."


GLOG_logtostderr=1 $TOOLS/convert_imageset \
  --resize_height=$RESIZE_HEIGHT \
  --resize_width=$RESIZE_WIDTH \
  --shuffle \
  --gray \
  $VAL_DATA_ROOT \
  $DATA/val.txt \
  $EXAMPLE/val_lmdb


echo "Done."

