import numpy as np
from image_source_canny import canny


def auto_canny(image, sigma = 0.33):
    """Zero-parameter, automatic Canny edge detection using scikit-image.
    Original function from pyimagesearch: Zero-parameter, automatic Canny edge with with Python and OpenCV
    www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv"""
        
    # compute the median of the single channel pixel intensities
    v = np.median(image)
 
    # apply automatic Canny edge detection using the computed median
    lower = float(max(0.0, (1.0 - sigma) * v))
    upper = float(min(1.0, (1.0 + sigma) * v))
    edged = canny(image, sigma, lower, upper)

    # return the edged image
    return edged