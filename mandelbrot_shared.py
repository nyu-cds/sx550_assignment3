# 
# A CUDA version to calculate the Mandelbrot set
#
from numba import cuda, int32
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

    Use shared memory to reduce communication overhead.
    '''
    y, x = cuda.grid(2)

    # Use shared memory to store constant values
    shared_height = cuda.shared.array(shape=(1), dtype=int32)
    shared_width = cuda.shared.array(shape=(1), dtype=int32)
    shared_height = image.shape[0]
    shared_width = image.shape[1]

    shared_pixel_size_x = cuda.shared.array(shape=(1), dtype=int32)
    shared_pixel_size_y = cuda.shared.array(shape=(1), dtype=int32)
    shared_pixel_size_x = (max_x - min_x) / shared_width
    shared_pixel_size_y = (max_y - min_y) / shared_height

    shared_r = cuda.shared.array(shape=(1), dtype=int32)
    shared_s = cuda.shared.array(shape=(1), dtype=int32)
    shared_r = blockdim[1] * griddim[1]
    shared_s = blockdim[0] * griddim[0]

    shared_r_range = cuda.shared.array(shape=(1), dtype=int32)
    shared_s_range = cuda.shared.array(shape=(1), dtype=int32)
    shared_r_range = (shared_width-1) // shared_r + 1
    shared_s_range = (shared_height-1) // shared_s + 1

    # Wait until all threads finish preloading
    cuda.syncthreads()
    
    # Every thread (y,x) will deal with points like (y+j*s, x+i*r)
    for i in range(shared_r_range):
        for j in range(shared_s_range):
            if shared_r * i + x < shared_width and shared_s * j + y < shared_height:
                real = min_x + (shared_r * i + x) * shared_pixel_size_x
                imag = min_y + (shared_s * j + y) * shared_pixel_size_y
                image[shared_s * j + y, shared_r * i + x] = mandel(real, imag, iters)


if __name__ == '__main__':
    image = np.zeros((1024, 1536), dtype = np.uint8)
    blockdim = (32, 8)
    griddim = (32, 16)
    
    image_global_mem = cuda.to_device(image)
    compute_mandel[griddim, blockdim](-2.0, 1.0, -1.0, 1.0, image_global_mem, 20) 
    image = image_global_mem.copy_to_host()
    imshow(image)
    show()