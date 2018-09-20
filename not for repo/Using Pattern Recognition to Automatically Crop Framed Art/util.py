import numpy as np

def sort_coords(raw_coords):
  '''
  Sorts an array of 4 coordinates, each an array w/ 2 numbers
  into counter-clockwise order starting from top left

  obvious solutions, sort by angle relative to center - doesn't always work - who knows why:
  coords = sorted(raw_coords, key = lambda p: (math.atan2(p[0] - center_x, p[1] - center_y) + 2 * math.pi) % 2*math.pi)
  '''
  left = sorted(raw_coords, key = lambda p: p[0])[0:2]
  right = sorted(raw_coords, key = lambda p: -p[0])[0:2]
  tl, bl = sorted(left, key = lambda p: p[1])
  tr, br = sorted(right, key = lambda p: p[1])
  return [tl, bl, br, tr]
