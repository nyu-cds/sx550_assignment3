# -----------------------------------------------------------------------------
# optimized version of calculator.py
# original runtime:     1.75 s
# optimized runtime:    24.4 ms
# speedup:  71.7x
# ----------------------------------------------------------------------------- 

import numpy as np


# For-loops are slow for matrix calculation
# Use build-in operators of numpy to speed up calculation
def hypotenuse(x,y):
    """
    Return sqrt(x**2 + y**2) for two arrays, a and b.
    x and y must be two-dimensional arrays of the same shape.
    """
    xx = np.multiply(x,x)
    yy = np.multiply(y,y)
    zz = np.add(xx, yy)
    return np.sqrt(zz)