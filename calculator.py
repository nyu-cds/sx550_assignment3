# -----------------------------------------------------------------------------
# optimized version of calculator.py
# original runtime:     1.75 s
# optimized runtime:    24.4 ms
# speedup:  71.7x
# ----------------------------------------------------------------------------- 

import numpy as np


# For-loops are slow for matrix calculation
# Use build-in operators of numpy to speed up calculation
def add(x,y):
    """
    Add two arrays using a Python loop.
    x and y must be two-dimensional arrays of the same shape.
    """
    return np.add(x,y)


def multiply(x,y):
    """
    Multiply two arrays using a Python loop.
    x and y must be two-dimensional arrays of the same shape.
    """
    return np.multiply(x,y)


def sqrt(x):
    """
    Take the square root of the elements of an arrays using a Python loop.
    """
    return np.sqrt(x)


def hypotenuse(x,y):
    """
    Return sqrt(x**2 + y**2) for two arrays, a and b.
    x and y must be two-dimensional arrays of the same shape.
    """
    xx = multiply(x,x)
    yy = multiply(y,y)
    zz = add(xx, yy)
    return sqrt(zz)