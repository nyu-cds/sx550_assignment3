"""
    N-body simulation.

    Combined all optimizations
    Original Runtime:               113.23277562403037 seconds
    Optimized Runtime:              33.16189348570092 seconds
    Optimized Runtime with jit:     2.9945386796120186 seconds
    Speedup to 1st optimized:       11.074124275461847x
    Optimized Runtime with jit&vec: 6.999645630469617 seconds
    Speedup to 1st optimized:       4.737653195091255x

    Vectorization slows down the program a lot. I guess vectorization leads to some overheads,
    which may be much more than performance improvement we get from vectorization.
"""
from itertools import combinations
from numba import jit, int32, float64, void, vectorize
import numpy as np


# Initialize BODIES and return it
@jit('float64[:,:,:]()')
def initialize():
    '''
        initialize statue of BODIES
    '''
    PI = 3.14159265358979323
    SOLAR_MASS = 4 * PI * PI
    DAYS_PER_YEAR = 365.24

    BODIES = np.array([
    ([0.0, 0.0, 0.0], 
     [0.0, 0.0, 0.0], 
     [SOLAR_MASS, 0.0, 0.0]),

    ([4.84143144246472090e+00,
      -1.16032004402742839e+00,
      -1.03622044471123109e-01],
     [1.66007664274403694e-03 * DAYS_PER_YEAR,
      7.69901118419740425e-03 * DAYS_PER_YEAR,
      -6.90460016972063023e-05 * DAYS_PER_YEAR],
     [9.54791938424326609e-04 * SOLAR_MASS,
      0.0,
      0.0]),

    ([8.34336671824457987e+00,
      4.12479856412430479e+00,
      -4.03523417114321381e-01],
     [-2.76742510726862411e-03 * DAYS_PER_YEAR,
      4.99852801234917238e-03 * DAYS_PER_YEAR,
      2.30417297573763929e-05 * DAYS_PER_YEAR],
     [2.85885980666130812e-04 * SOLAR_MASS,
      0.0,
      0.0]),

    ([1.28943695621391310e+01,
      -1.51111514016986312e+01,
      -2.23307578892655734e-01],
     [2.96460137564761618e-03 * DAYS_PER_YEAR,
      2.37847173959480950e-03 * DAYS_PER_YEAR,
      -2.96589568540237556e-05 * DAYS_PER_YEAR],
     [4.36624404335156298e-05 * SOLAR_MASS,
      0.0,
      0.0]),

    ([1.53796971148509165e+01,
      -2.59193146099879641e+01,
      1.79258772950371181e-01],
     [2.68067772490389322e-03 * DAYS_PER_YEAR,
      1.62824170038242295e-03 * DAYS_PER_YEAR,
      -9.51592254519715870e-05 * DAYS_PER_YEAR],
     [5.15138902046611451e-05 * SOLAR_MASS,
      0.0,
      0.0])
    ], dtype=np.float64)

    return BODIES


@vectorize([float64(float64, float64)])
def vec_deltas(x, y):
    return x - y


# Add iterations
# Add BODIES to parameters
@jit('void(float64, int32, float64[:,:,:], int32[:,:])', nopython=True)
def advance(dt, iterations, BODIES, cached_body_pairs):
    '''
        advance the system one timestep
    '''
    for _ in range(iterations):
        # Remove nested for-loop with cached body pairs
        for index in range(len(cached_body_pairs)):
            (body1, body2) = cached_body_pairs[index]
            r1 = BODIES[body1, 0]
            v1 = BODIES[body1, 1]
            m1 = BODIES[body1, 2, 0]
            r2 = BODIES[body2, 0]
            v2 = BODIES[body2, 1]
            m2 = BODIES[body2, 2, 0]
            
            # Compute deltas
            (dx, dy, dz) = vec_deltas(r1, r2)
            
            # Update vs
            # Compute mag, b2 and b1 first
            mag = dt * ((dx * dx + dy * dy + dz * dz) ** (-1.5))
            b2 = m2 * mag
            b1 = m1 * mag
            v1[0] -= dx * b2
            v1[1] -= dy * b2
            v1[2] -= dz * b2
            v2[0] += dx * b1
            v2[1] += dy * b1
            v2[2] += dz * b1
            
        for body in range(len(BODIES)):
            r = BODIES[body, 0]
            v = BODIES[body, 1]

            # Update rs
            r += dt * v


# Add BODIES and cached_body_pairs to parameters
@jit('float64(float64[:,:,:], int32[:,:], float64)', nopython=True)
def report_energy(BODIES, cached_body_pairs, e=0.0):
    '''
        compute the energy and return it so that it can be printed
    '''
    
    # Remove nested for-loop with cached body pairs
    for index in range(len(cached_body_pairs)):
        (body1, body2) = cached_body_pairs[index]
        r1 = BODIES[body1, 0]
        m1 = BODIES[body1, 2, 0]
        r2 = BODIES[body2, 0]
        m2 = BODIES[body2, 2, 0]

        # Compute deltas
        (dx, dy, dz) = vec_deltas(r1, r2)

        # Compute energy
        e -= (m1 * m2) / ((dx * dx + dy * dy + dz * dz) ** 0.5)
        
    for body in range(len(BODIES)):
        vx = BODIES[body, 1, 0]
        vy = BODIES[body, 1, 1]
        vz = BODIES[body, 1, 2]
        m = BODIES[body, 2, 0]
        e += m * (vx * vx + vy * vy + vz * vz) / 2.
        
    return e


# Add BODIES to parameters
@jit('void(int32, float64[:,:,:], float64, float64, float64)', nopython=True)
def offset_momentum(ref, BODIES, px=0.0, py=0.0, pz=0.0):
    '''
        ref is the body in the center of the system
        offset values from this reference
    '''
    for body in range(len(BODIES)):
        vx = BODIES[body, 1, 0]
        vy = BODIES[body, 1, 1]
        vz = BODIES[body, 1, 2]
        m = BODIES[body, 2, 0]
        px -= vx * m
        py -= vy * m
        pz -= vz * m
        
    v = BODIES[ref, 1]
    m = BODIES[ref, 2, 0]
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m

    # Add returned value
    #return BODIES
    

@jit('void(int32, int32, int32)')
def nbody(loops, reference, iterations):
    '''
        nbody simulation
        loops - number of loops to run
        reference - body at center of system
        iterations - number of timesteps to advance
    '''
    # Set up global state
    BODIES = initialize()  

    # Generator all body pairs
    cached_body_pairs = np.array(list(combinations(range(5), 2)), dtype=np.int32)

    # Add BODIES to parameters
    offset_momentum(reference, BODIES, 0.0, 0.0, 0.0)

    for _ in range(loops):
        # Move loop into advance()
        advance(0.01, iterations, BODIES, cached_body_pairs)
        print(report_energy(BODIES, cached_body_pairs, 0.0))


if __name__ == '__main__':

    # Compute total runtime for 1 run
    import timeit
    print(timeit.timeit("nbody(100, 0, 20000)", setup="from __main__ import nbody", number=1))
