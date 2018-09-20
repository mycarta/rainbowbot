import numpy as np
import scipy as sp
from scipy import ndimage as ndi
from skimage import color, feature
from skimage.filters import threshold_otsu
from skimage.morphology import remove_small_objects, disk, opening
from skimage.measure import find_contours, approximate_polygon
from skimage import transform as tf

def find_largest(img, threshold = 'global'):
    """Function to find largest bright object in an image. Workflow:
    - 	Convert input to binary with threshold. 
    -	Find and retain only largest object in binary image
    -	Fill holes
    -	Apply opening and dilation to remove minutiae"""
    
    # Apply threshold
    # Options: 'global' (default) applies global Otsu thresholding 
    #          'tips' eliminates both ~black and ~nearly white backgrounds
    #          'textural' eliminates backgrounds of (any) constant colour - NOT AVAILABLE YEY   
    if threshold == 'tips':
        binary = np.logical_and(color.rgb2gray(img) > 0.05, color.rgb2gray(img) < 0.95) 
    global_thresh = threshold_otsu(img)
    binary = img < global_thresh
    
    # Detect largest bright element in the binary image. Making the assumption it would be the map.
    # Eliminate everything else (text, colorbar, holes, ...).
    # Label all white objects (made up of ones)
    label_objects, nb_labels = ndi.label(binary) # ndimage.label actually labels 0 (background) as 0 and then 
                                                        # labels every nonzero object as 1, 2, ... n. 
    # Calculate every labeled object's size. 
    # np.bincount ignores whether input is an image or another type of array.
    # It just calculates the binary sizes, including for the 0 (background).
    sizes = np.bincount(label_objects.ravel())   
    sizes[0] = 0    # This sets the size of the background to 0 so that if it happened to be larger than 
                    # the largest white object it would not matter
   
    # Keep only largest object
    binary_objects = remove_small_objects(binary, max(sizes)) 
    
    # Remove holes from it (black regions inside white object)
    binary_holes = ndi.morphology.binary_fill_holes(binary_objects) 
    
    # This may help remove minutiae on the outside (tick marks and tick labels)
    binary_mask = opening(binary_holes, disk(7))
    return binary_mask

def ordered(points):
    """Function to sort corners based on angle from centroid. 
       Modified from: http://stackoverflow.com/a/31235064/1034648"""
    x = points[:,0]
    y = points[:,1]
    cx = np.mean(x)
    cy = np.mean(y)
    a = np.arctan2(y - cy, x - cx)
    order = a.ravel().argsort()
    x = x[order]
    y = y[order]
    return np.vstack([x,y])

def rectify_seismic(img, binary_mask):
    """Function to warp to a rectangle the area in the input img defined by binary_mask 
    It returns the warped area as an image"""
    
    # Find mask contour, approximate it with a quadrilateral, find and sort corners
    contour = np.squeeze(find_contours(binary_mask, 0))
    coords = approximate_polygon(contour, tolerance=50)
    
    # sort the corners with the exception of the last one (repetition of first corner)
    sortedCoords = ordered(coords[:-1]).T
    
    # Define size of output image based on largest width and height in the input
    w1 = np.sqrt(((sortedCoords[0, 1]-sortedCoords[3, 1])**2)+((sortedCoords[0, 0]-sortedCoords[3, 0])**2))
    w2 = np.sqrt(((sortedCoords[1, 1]-sortedCoords[2, 1])**2)+((sortedCoords[1, 0]-sortedCoords[2, 0])**2))
    h1 = np.sqrt(((sortedCoords[0, 1]-sortedCoords[1, 1])**2)+((sortedCoords[0, 0]-sortedCoords[1, 0])**2))
    h2 = np.sqrt(((sortedCoords[3, 1]-sortedCoords[2, 1])**2)+((sortedCoords[3, 0]-sortedCoords[2, 0])**2))
    w = max(int(w1), int(w2))
    h = max(int(h1), int(h2))
    
    # Define rectangular destination coordinates (homologous points) for warping
    dst = np.array([[0, 0],
                    [h-1, 0],
                    [h-1, w-1],
                    [0, w-1]], dtype = 'float32')
    
    # Estimate warping transform, apply to input image (mask portion), and output
    dst[:,[0,1]] = dst[:,[1,0]]
    sortedCoords[:,[0,1]] = sortedCoords[:,[1,0]]
    tform = tf.ProjectiveTransform()
    tform.estimate(dst,sortedCoords)
    warped = tf.warp(img, tform, output_shape=(h-1, w-1))
    return warped
    
    
    