# Script for resizing images to 200x150 using tensorflow image operations
import os
import numpy as np
import tensorflow as tf
from PIL import Image

print('[ read images ]')
image_dir='../data/resizing-test-data/test-images'
im_filenames=os.listdir(image_dir)
image_paths=[image_dir + '/' + fname for fname in im_filenames]

count = 0;
print('[ resize images ]')
for image_path in image_paths:
  image_raw = tf.io.read_file(image_path)
  image = tf.image.decode_jpeg(image_raw)
  image_lg = tf.image.resize_with_crop_or_pad(image, 799, 600)
  image_sm = tf.image.resize_with_pad(image_lg, 200, 150)
  print(image_sm.shape)
  image_jpg = tf.io.encode_jpeg(tf.cast(image_sm, tf.uint8))
  tf.io.write_file('../data/resizing-test-data/small-images/out{}.jpg'.format(count), image_jpg)
  count += 1
    
