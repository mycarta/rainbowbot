import cv2
import numpy as np
from lib.util import sort_coords, format
import math

def skew(pt1,pt2):
  '''
  expects two points vertically separated. If your points are horizontally
  separated, reverse their x and y when passing into this function
  output is the angle between the line the two points make and the horizontal

  An output of 90 means the input line is below and normal to the horizontal
  A positive output means the input line is below horizontal and makes an
  acute angle to the horizontal on its right, and obtuse on its left
  A negative output means the input line is below horizontal and makes an
  obtuse angle to the horizontal on its right, and acute on its left
  '''
  a1,b1 = pt1; a2,b2 = pt2;
  if a2 == a1:
    return 90
  else:
    return (math.atan((b1 - b2) / (a1 - a2)) * 180 / np.pi)
