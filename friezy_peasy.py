"""
A frieze generator.
"""

__docformat__ = 'restructuredtext'

import cv2 as cv
import numpy as np

import argparse

MAX_LINE = 60
PATTERNS = ['p1', 'p2', 'p1m1', 'p2mm', 'p11m', 'p11g', 'pcm', 'p2mg']

def build_frieze(im, pattern, nreps):
  """
  Generate the frieze image given an UIC frieze pattern and the number
  of repetitions of the image.

  :param im: Image 
  :type im: cv.Mat
  :param pattern: Frieze pattern
  :type pattern: str
  :param nreps: Number of times the unit cell is repeated along the
  frieze. The possible values are:

          1. ``'p1'``
          2. ``'p2'``
          3. ``'p1m1'``
          4. ``'p2mm'``
          5. ``'p11m'``
          6. ``'p11g'``
          7. ``'pcm'`` or ``'p2mg'``

  :type nreps: int
  :rparam Array of concatenated unit cells that represents the frieze.
  :rtype list
  """
  
  if(pattern == 'p1'):
    unit_cell = [im]
    
  elif(pattern == 'p2'):
    unit_cell = [im, cv.rotate(im, cv.ROTATE_180)]
    
  elif(pattern == 'p1m1'):
    
    # 1 = vertical line reflection
    # 0 = horizontal line reflection
    unit_cell = [im, cv.flip(im, 1)]
    
  elif(pattern == 'p2mm'):
    
    unit_cell = [np.concatenate((im, cv.flip(im, 0)), axis=0)]
    unit_cell.append(np.flip(unit_cell[0], 1))

  elif(pattern == 'p11m'):
    unit_cell = [np.concatenate((im, cv.flip(im, 0)), axis=0)]

  elif(pattern == 'p11g'):
    
    im2 = cv.flip(im, 0)
    firsthalf = im2[:, 0:int(im2.shape[1] / 2)]
    secondhalf = im2[: , int(im2.shape[1] / 2):int(im2.shape[1])]

    # Snap horizontally two images
    im3 = np.concatenate((secondhalf, firsthalf), axis=1)
    im4 = np.concatenate((im, im3), axis=0)
    unit_cell = [im4]

  elif(pattern in ('pcm', 'p2mg')):
    
    unit_cell = [np.concatenate((im, cv.flip(im, 1)), axis=1)]
    unit_cell.append(cv.rotate(unit_cell[0], cv.ROTATE_180))

  return np.hstack(unit_cell * nreps)


if __name__ == '__main__':

  parser = argparse.ArgumentParser(
    prog='friezy_peasy',
    description='Frieze images generator')

  parser.add_argument(
    'im_path',
    metavar='image-path',
    help='Path to the image used to generate the frieze.')

  parser.add_argument(
    'output_path',
    metavar='destiny-path',
    help='Path to the file where the generated image will be saved.')

  parser.add_argument(
    'pattern',
    choices=PATTERNS,
    metavar='pattern',
    help='IUCr frieze pattern group that will be used to generate the frieze.')

  parser.add_argument(
    'nreps',
    choices=range(1, MAX_LINE // 2 + 1),
    type=int,
    metavar='N',
    help='Number of times the resulting frieze image will be repeated.')

  args = parser.parse_args()
  im = cv.imread(args.im_path)
  output_im = build_frieze(im, args.pattern, args.nreps)
  cv.imwrite(args.output_path, output_im)
