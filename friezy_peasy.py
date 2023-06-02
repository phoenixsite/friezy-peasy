"""
A frieze generator.
"""

__docformat__ = 'restructuredtext'

import cv2 as cv
import numpy as np

import argparse

MAX_LINE = 60

def saveImage(im, output_path):
  """
  Save the generated image to a file.

  :param im: Array of concatenated unit cells
  :type im: numpy.ndarray
  :param output_path: Path route where the image is saved.
  :type: str
  """
  
  im = np.hstack(im)
  cv.imwrite(output_path, im)

def buildFrieze(im, pattern, nreps):
  """
  Generate the frieze image given an UIC frieze pattern and the number
  of repetitions of the image.

  :param im: Image 
  :type im: cv.Mat
  :param pattern: UIC frieze pattern
  :type pattern: str
  :type nreps: Number of times the unit cell is repeated along the
  frieze.
  :rparam Array of concatenated unit cells that represents the frieze.
  :rtype list
  """
  
  if(pattern == 'p1'):
    unit_cell = [im]
    
  elif(pattern == 'p2'):
    
    im2 = cv.rotate(im, cv.ROTATE_180)
    unit_cell = [im, im2]
    
  elif(pattern == 'p1m1'):
    
    # 1 = vertical line reflection
    # 0 = horizontal line reflection
    im2 = cv.flip(im, 1)
    unit_cell = [im, im2]
    
  elif(pattern == 'p2mm'):
    
    im2 = cv.flip(im, 0)

    # Snap vertically two images
    im3 = np.concatenate((im, im2), axis=0)
    im4 = np.flip(im3, 1)
    unit_cell = [im3, im4]

  elif(pattern == 'p11m'):
    
    im2 = cv.flip(im, 0)
    im3 = np.concatenate((im, im2), axis=0)
    unit_cell = [im3]

  elif(pattern == 'p11g'):
    
    im2 = cv.flip(im, 0)
    firsthalf = im2[:, 0:int(im2.shape[1] / 2)]
    secondhalf = im2[: ,int(im2.shape[1] / 2):int(im2.shape[1])]

    # Snap horizontally two images
    im3 = np.concatenate((secondhalf,firsthalf), axis=1)
    im4 = np.concatenate((im,im3), axis=0)
    unit_cell = [im4]
    
  elif(pattern == 'pcm'):
    
    im2 = cv.flip(im, 1)
    im3 = np.concatenate((im, im2), axis=1)
    im4 = cv.rotate(im3, cv.ROTATE_180)
    unit_cell = [im3, im4]

  else:
    raise RuntimeException("The given pattern is not valid")

  out = []
  for i in range(nreps):
    out.extend(unit_cell)

  return out


if __name__ == '__main__':

  parser = argparse.ArgumentParser(
    prog='friezy_peasy',
    description='Frieze images generator')

  pattern_choices = ['p1', 'p2', 'p1m1', 'p2mm', 'p11m', 'p11g', 'pcm']

  parser.add_argument(
    'im_path',
    metavar='image-path',
    help='Image path which is used to generate the frieze.')

  parser.add_argument(
    'output_path',
    metavar='destiny-path',
    help='Destiny image path where the generated image will be saved.')

  parser.add_argument(
    'pattern',
    choices=pattern_choices,
    metavar='pattern',
    help='Frieze pattern group that will be used to generate the frieze.')

  parser.add_argument(
    'nreps',
    choices=range(1, MAX_LINE // 2 + 1),
    type=int,
    metavar='N',
    help='Number of times the resulting frieze image will be repeated.')

  args = parser.parse_args()
  im = cv.imread(args.im_path)
  output_im = buildFrieze(im, args.pattern, args.nreps)
  saveImage(output_im, args.output_path)
