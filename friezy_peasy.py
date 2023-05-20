# -*- coding: utf-8 -*-

import cv2, numpy as np, math
import matplotlib.image as mp_image

import argparse

MAX_LINE = 20

def readIm(filename, flagColor=1):

  if(flagColor!=1 and flagColor!=0):
    print("Valor no válido de flagColor, se asignará directamente el valor 1")
    flagColor=1

  return cv2.cvtColor(cv2.imread(filename,flagColor), cv2.COLOR_BGR2RGB)

def rangeDisplay01(im, flag_GLOBAL):

  #check image type (grayscale or color)
  bands = len(im.shape)
  max = np.max(im)
  min = np.min(im)
  dif = max-min
  im2 = np.copy(im)
  if (flag_GLOBAL==True or bands!=3):
  # normalize the grayscale image
  # compute range and apply normalization
    im2 = (im2-min)/dif
  else:
    # normalize each band as a grayscale image 
    for k in range(im2.shape[2]):
      max = np.max(im2[:,:,k])
      min = np.min(im[:,:,k])
      dif = max-min
      for i in range(im2.shape[1]): #columns
          for j in range(im2.shape[2]): #RGB
            im2[i][j][k] = (im2[i][j][k]-min)/dif
  return im2

def saveImage(vim, output_path):
  
  size = len(vim)
  if size <= MAX_LINE:
    out = np.hstack(vim)
    out = np.asarray(out,float)
  else:
    times = round(size / MAX_LINE)
    rest = size % MAX_LINE
    if (rest >= MAX_LINE / 2):
      times = times - 1
    aux = []
    for i in range(times):
      auxvim = []
      for j in range(MAX_LINE):
        auxvim.append(vim[i * MAX_LINE + j])
      aux.append(np.hstack(auxvim))
    if(rest!=0):
      #We have to add black figures to match the size of the rest of the arrays
      blackimage = np.full((len(vim[0]),len(vim[0][0]),3),[0,0,0])
      auxvim = []
      for i in range(rest):
        auxvim.append(vim[times * MAX_LINE +i])
      for i in range(MAX_LINE - rest):
        auxvim.append(blackimage)
      aux.append(np.hstack(auxvim))
    out = np.vstack(aux)
    out = np.asarray(out,float)

  # Normalize range
  im2 = np.copy(out)
  im2 = np.asarray(im2, float)
  im2 = rangeDisplay01(im2, True)
  mp_image.imsave(output_path, im2)

def buildFriso(im, type, nreps):
  """Generate the frieze image given its type and the number of repetitions
  of the image.
  """

  result_image = []
  
  if(type == 'p1'):
    unit_cell = [im]
    
  elif(type == 'p2'):
    im2 = cv2.rotate(im,cv2.ROTATE_180)
    unit_cell = [im, im2]
    
  elif(type=='p1m1'):
    im2 = cv2.flip(im, 1)     #1=reflexión con recta vertical, 0 = reflexión con recta horizontal
    unit_cell = [im, im2]
    
  elif(type=='p2mm'):
    im2 = cv2.flip(im,0)
    im3 = np.concatenate((im,im2), axis=0)  #Pegar 2 imágenes verticalmente
    im4 = np.flip(im3,1)
    unit_cell = [im3, im4]

  elif(type=='p11m'):
    im2 = cv2.flip(im,0)
    im3 = np.concatenate((im,im2), axis=0)
    unit_cell = [im3]

  elif(type=='p11g'):
    im2 = cv2.flip(im,0)
    firsthalf = im2[:,0:int(im2.shape[1]/2)]
    secondhalf = im2[:,int(im2.shape[1]/2):int(im2.shape[1])]
    im3 = np.concatenate((secondhalf,firsthalf), axis=1)    #Pegar 2 imágenes horizontalmente
    im4 = np.concatenate((im,im3), axis=0)
    unit_cell = [im4]
    
  elif(type=='pcm'):
    im2 = cv2.flip(im,1)
    im3 = np.concatenate((im,im2), axis=1)
    im4 = cv2.rotate(im3, cv2.ROTATE_180)
    unit_cell = [im3, im4]

  for i in range(nreps):
    result_image.extend(unit_cell)

  return result_image


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
  im = readIm(args.im_path, 1)
  output_im = buildFriso(im, args.pattern, args.nreps)
  saveImage(output_im, args.output_path)
