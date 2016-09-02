import numpy as np
from PIL import Image
import requests
from StringIO import StringIO
from scipy import ndimage as ndi
from skimage import color
from skimage.morphology import disk, opening, remove_small_objects


def find_map(url, min_int = 0.03, max_int = 0.97, disk_sz = 3):
    """Find the map in an image (using morphological operations) and return it.
    Heuristic assumption the map is the largest object in the map.
    Parameters
    ----------
    img: (M, N, 3) or (M, N, 4) 
        An RGB or RGBA image.
    min_int : threshold value to eliminate ~black background.
        If min_int is not given, a default value of 0.03 is uded.
    max_int : threshold value to eliminate ~white background.
        If max_int is not given, a default value of 0.97 is uded. 
    disk_sz : size of disk-shaped structuring element for opening.
        If disk_sz is not given, a default value of 3 is uded.
    Returns
    -------
    out : (M, N, 3) array
        An image with only the main map.    
    """

    # rgb from url
    rspns = requests.get(url)
    img = np.asarray(Image.open(StringIO(rspns.content)))[:,:,:3]
    
    # image must be RGB or RGB(A)
    if not len(img.shape) > 2:
        raise ValueError('Sorry, image has to be RGB (M, N, 3) or RGBA (M, N, 4)')

    # remove alpha channel
    img = img[:,:,:3]
    
    # binary from rgb
    binary = np.logical_and(color.rgb2gray(img) > 0.03, color.rgb2gray(img) < 0.97)
    
    # apply very mild opening
    binary = opening(binary, disk(disk_sz))
    
    # keep only largest white object
    label_objects, nb_labels = ndi.label(binary)
    sizes = np.bincount(label_objects.ravel())   
    sizes[0] = 0   
    if nb_labels <2: # background not included in the count
        binary_objects = binary # in case the image already contained only the map
    else:
        binary_objects = remove_small_objects(binary, max(sizes))  
    
    # remove holes from it
    binary_holes = ndi.morphology.binary_fill_holes(binary_objects) 
    
    # use it to make 3D mask
    mask3 = np.zeros(img.shape)
    mask3[:,:,0] = binary_holes
    mask3[:,:,1] = binary_holes
    mask3[:,:,2] = binary_holes
    
    # use mask to get only map in original image
    final = np.ma.masked_where(mask3 ==0, img)
    final = final.filled(0)
    
    # crop zero columns and zero rows
    # see http://stackoverflow.com/a/31402351/1034648
    non_empty = np.where(final != 0)
    out = final[np.min(non_empty[0]) : np.max(non_empty[0]), 
                   np.min(non_empty[1]) : np.max(non_empty[1])]
    
    # output
    return out