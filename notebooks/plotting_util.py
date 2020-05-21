import matplotlib.pyplot as plt
import numpy as np
import os

def remove_ticks(ax):
  """
  Remove axes tick labels
  """
  ax.set_xticklabels([])
  ax.set_yticklabels([])
  ax.set_xticks([])
  ax.set_yticks([])

def plot_classification_examples(prediction, actual, im, count=10):
  """
  Plot sample images with predictions and actual labels
  """
  labels = load_labels()
  plot_labeled_class_examples(prediction, lables, actual, im, count)

def load_labels():
    theaters = open(os.path.abspath("../scripts/theaters.txt")).read().split('\n')
    return theaters

def plot_labeled_class_examples(prediction, labels, actual, im, count=10):
  fh = plt.figure()
  fh.set_figheight(10)
  fh.set_figwidth(15)
  num_test=actual.shape[0]
  for i in range(count):
    ax=plt.subplot(2,5,i+1)
    remove_ticks(ax)
    lh=plt.xlabel(labels[np.argmax(prediction[i])])
    if (np.argmax(prediction[i])==np.argmax(actual[i])):
      lh.set_color('green')
    else:
      lh.set_color('red')
    plt.imshow(im[i])
    