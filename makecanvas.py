from PIL import Image
import sys, os

def main():
  im = Image.new('RGB', (512,512), "white")
  im.save('canvas.jpg')


if __name__ == '__main__':
  main()
