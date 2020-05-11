# Script for resizing images to 200x150 using tensorflow image operations
import os
import tensorflow as tf


def resize_img_for_theater(theater):
  dir_name = theater.replace(" ", "")
  image_dir=os.path.abspath('../data/' + dir_name)
  if not os.path.exists(image_dir):
    print('no images found')
    return
  image_filenames=os.listdir(image_dir)
  image_paths=[image_dir + '/' + name for name in image_filenames]

  count = 0;
  print('resizing ', len(image_paths), ' images')
  for image_path in image_paths:
    image_raw = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image_raw)
    image_lg = tf.image.resize_with_crop_or_pad(image, 799, 600)
    image_sm = tf.image.resize_with_pad(image_lg, 200, 150)
    image_jpg = tf.io.encode_jpeg(tf.cast(image_sm, tf.uint8))
    tf.io.write_file('../resized-data/{}/out{}.jpg'.format(dir_name, count), image_jpg)
    count += 1

theaters = open(os.path.abspath("../data/theaters.txt")).read().split('\n')

for theater in theaters:
    if len(theater) > 1:
        print("resizing for:", theater)
        resize_img_for_theater(theater)
