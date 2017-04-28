# 
# A CUDA version to calculate the Mandelbrot set
#
from numba import cuda
import numpy as np
from pylab import imshow, show

@cuda.jit(device=True)
def mandel(x, y, max_iters):
    '''
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the 
    Mandelbrot set given a fixed number of iterations.
    '''
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return i

    return max_iters

@cuda.jit
def compute_mandel(min_x, max_x, min_y, max_y, image, iters):
    '''
    Note: I use (y,x) to get position to keep consistant with the original code,
    rather than (x,y).

    Every thread (y,x) will deal with points like (y+j*s, x+i*r) within the image,
    so that the program can cover the whole image without repetition,
    where s = blockdim[0] * griddim[0], r = blockdim[1] * griddim[1].
    
    For each (y+j*s, x+i*r), compute corresponding real and image in the same way
    of the original code, and use mandel() to determine if it is in the Mandelbrot set.
    '''
    y, x = cuda.grid(2)

    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height

    r = blockdim[1] * griddim[1]
    s = blockdim[0] * griddim[0]

    r_range = (width-1) // r + 1
    s_range = (height-1) // s + 1

    for i in range(r_range):
        for j in range(s_range):
            if r * i + x < width and s * j + y < height:
                real = min_x + (r * i + x) * pixel_size_x
                imag = min_y + (s * j + y) * pixel_size_y
                image[s * j + y, r * i + x] = mandel(real, imag, iters)

if __name__ == '__main__':
    image = np.zeros((1024, 1536), dtype = np.uint8)
    blockdim = (32, 8)
    griddim = (32, 16)
    
    image_global_mem = cuda.to_device(image)
    compute_mandel[griddim, blockdim](-2.0, 1.0, -1.0, 1.0, image_global_mem, 20) 
    image = image_global_mem.copy_to_host()
    imshow(image)
    show()