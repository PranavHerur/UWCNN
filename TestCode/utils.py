"""
Scipy version > 0.18 is needed, due to 'mode' option from scipy.misc.imread function
"""

import os
import glob
import h5py
import random
import imageio
import matplotlib.pyplot as plt

from PIL import Image  # for loading images as YCbCr format
import scipy.misc
import scipy.ndimage
import numpy as np

import tensorflow as tf

FLAGS = tf.compat.v1.app.flags.FLAGS

def transform(images):
  return np.array(images)/127.5 - 1.

def inverse_transform(images):
  return (images+1.)/2

def prepare_data(sess, dataset):
  """
  Args:
    dataset: choose train dataset or test dataset
    
    For train dataset, output data would be ['.../t1.bmp', '.../t2.bmp', ..., '.../t99.bmp']
  
  """

  filenames = os.listdir(dataset)
  data_dir = os.path.join(os.getcwd(), dataset)
  data = glob.glob(os.path.join(data_dir, "*.bmp"))
  data = data + glob.glob(os.path.join(data_dir, "*.jpg"))
  return data

def imread(path, is_grayscale=False):
  """
  Read image using its path.
  Default value is gray-scale, and image is read by YCbCr format as the paper said.
  """
  if is_grayscale:
    return imageio.imread(path, as_gray=True).astype(float)
  else:
    return imageio.imread(path).astype(float)

    
def imsave(image, path):

  imsaved = (inverse_transform(image)).astype(np.float)
  return scipy.misc.imsave(path, imsaved)

def get_image(image_path,is_grayscale=False):
  image = imread(image_path, is_grayscale)

  return transform(image)

def get_label(image_path,is_grayscale=False):
  image = imread(image_path, is_grayscale)
  return image/255.

def imsave_label(image, path):
    # Ensure values are in [0, 1] range
    image = np.clip(image, 0, 1)
    # Convert float array to uint8 before saving
    image_uint8 = (image * 255).astype(np.uint8)
    return imageio.imsave(path, image_uint8)
