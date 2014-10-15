# Andrea Compton
# 9/16/14
# Concurrent Programming
# Transform_image: takes in an images and transforms it according 
#   to the provided function
# Synchronization required: None. This is because each thread operates
#   on a different portion of the picture and there is no chance of
#   them overlapping

from __future__ import print_function
import threading, os, sys
from PIL import Image

MAX_THREADS = 100


def makeBlue(tuple):
  """
    changes the red value to be the blue value
  """
  r, g, b = tuple
  return (b, g, b)

def switch_r_b(tuple):
  """
    switches the red and blue values
  """
  r, g, b = tuple
  return (b, g, r)

def switch_b_g(tuple):
  """
    switches the green and blue values
  """
  r, g, b = tuple
  return (r, b, g)

def get_init_row_limit(rows, height):
  """
    get number of rows each thread will traverse
  """
  perThread = height / rows
  if height % rows != 0: perThread += 1
  return perThread

def get_init_col_limit(cols, width):
  """
    get number of cols each thread will traverse
  """
  perThread = width / cols
  if width % cols != 0: perThread += 1
  return perThread

def transform_function(transformation):
  """
    makes sure the transformation is valid and returns the function value
  """
  if transformation in transformDict:
    return transformDict[transformation]
  else:
    print('Unknown transform: ' + transformation, file=sys.stderr)
    exit(1)

def get_image(image):
  """
    makes sure the image is the correct type
  """
  file = Image.open(image)
  if file.format != 'JPEG' or file.mode != 'RGB':
    print('Wrong image type', file=sys.stderr)
    exit(1)
  return file
    
def create_threads(pix_map, func, row, rowlim, col, collim):
  """
    for each pixel, call the specified function
  """
  for c in range(col, collim):
    for r in range(row, rowlim):
      pix_map[c, r] = func(pix_map[c, r])

def transform_image(image, name, transformation, rows=2, cols=2):
  """
    creates correct number of threads, which transform image, then saves it
  """
  rows = int(rows)
  cols = int(cols)
  numThreads = rows*cols
  if numThreads > MAX_THREADS:
    print('Rows and cols will created too many threads', file=sys.stderr)
    exit(1)
  
  newImage = get_image(image)
  pix_map = newImage.load()
  width, height = newImage.size
  transformFunc = transform_function(transformation)
  rowmax = get_init_row_limit(rows, height)
  colmax = get_init_col_limit(cols, width)
  threads = []

  if numThreads >= (width*height):
    rows = height
    cols = width
    rowmax = 1
    colmax = 1

  for c in range(cols):
    for r in range(rows):
      row = r * rowmax
      col = c * colmax
      rowlim = (r+1)*rowmax
      collim = (c+1)*colmax
      if rowlim >= height: rowlim = height
      if collim >= width: collim = width
      thread = threading.Thread(target=create_threads, 
                    args=[pix_map,transformFunc,row, rowlim, col, collim])
      thread.start()
      threads.append(thread)
  for thread in threads:
    thread.join()
  newImage.save(name)

def get_args(args):
  """
    Gets the number of arguments and calls transform_image
  """
  if len(args) == 6:
    if int(args[4]) == 0 or int(args[5]) == 0:
      print('Cannot have a zero value', file=sys.stderr)
      exit(1)
    else:
      transform_image(args[1], args[2], args[3], args[4], args[5])
  elif len(args) == 4:
    transform_image(args[1], args[2], args[3], 2, 2)
  else:
    print('Must have 3 or 5 inputs', file=sys.stderr)

def main(args):
  get_args(args)

transformDict = {
  'switch-r-b': switch_r_b,
  'switch_b_g': switch_b_g,
  'makeBlue': makeBlue
}

if __name__ == '__main__':
  main(sys.argv)

