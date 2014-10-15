# Andrea Compton
# 9/17/14
# Concurrent Programming
# procedural_artist: create an image using the specified
#  number of threads and steps for each thread, each step
#  representing an artist painting one pixel

import threading, os, sys, random
from PIL import Image
from mutex import mutex
from multiprocessing import Process, Lock

height = 512
width = 512
canvas = []
mutex = Lock()

def paintColor(color, newpos, list):
  if canvas[newpos] == (255, 255, 255):
    canvas[newpos] = color
  else:
    newpos = random.choice(list)
    
  return newpos

def startpaint(color, position, list, attempts):
  """
    called when thread is started
  """
  for attempt in range(attempts):
    if position is None: position = random.choice(list)
    list.append(position)
    mutex.acquire()
    x, y = paintColor(color, position, list)
    mutex.release()
    position = paint2((x, y))
  return

def paint2(position):
  x, y = position
  dir = random.randint(0, 4)
  if dir == 0: 
    if x-1 >= 0:
      return (x-1, y)

  elif dir == 1:
    if y-1 >= 0:
      return (x, y-1)

  elif dir == 2: 
    if x+1 < (height-1):
      return (x+1, y)

  elif dir == 3: 
    if y+1 < (width-1):
      return (x, y+1)

def assignPosition():
  x = random.randint(0, height-1)
  y = random.randint(0, width-1)
  return (x, y)

def assignColor():
  r = random.randint(0, 255)
  g = random.randint(0, 255)
  b = random.randint(0, 255)
  if (r, g, b) == (255, 255, 255): assignColor
  return (r, g, b)

def main(args):
  image = Image.open('canvas.jpg')
  global canvas
  canvas = image.load()
  colors = []
  positions = []
  threads = []
  if args[1] == '-M':
    numThreads = int(args[2])
    attempts = int(args[4])
  else: 
    numThreads = int(args[4])
    attempts = int(args[2])
  for n in range(numThreads):
    list = []
    color = assignColor()
    mutex.acquire()
    position = assignPosition()
    mutex.release()
    while color in colors:
      color = assignColor()
    while position in positions:
      position = assignPosition()
    thread = threading.Thread(target=startpaint, 
                    args=[color, position, list, attempts])
    thread.start()
    threads.append(thread)
  
  for thread in threads: thread.join()
  
  image.save('masterpiece.jpg')

if __name__ == '__main__':
  main(sys.argv)

