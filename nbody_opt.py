"""
    N-body simulation.

    Combined all optimizations
    Original Runtime:   566.1638781201518 / 5 = 113.23277562403037 seconds
    Optimized Runtime:  165.8094674285046 / 5 = 33.16189348570092 seconds
    Speedup:    3.4145449406516915x
"""
from itertools import combinations


# Initialize BODIES and return it
def initialize():
    '''
        initialize statue of BODIES
    '''
    PI = 3.14159265358979323
    SOLAR_MASS = 4 * PI * PI
    DAYS_PER_YEAR = 365.24

    BODIES = {
    'sun': ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], SOLAR_MASS),

    'jupiter': ([4.84143144246472090e+00,
                 -1.16032004402742839e+00,
                 -1.03622044471123109e-01],
                [1.66007664274403694e-03 * DAYS_PER_YEAR,
                 7.69901118419740425e-03 * DAYS_PER_YEAR,
                 -6.90460016972063023e-05 * DAYS_PER_YEAR],
                9.54791938424326609e-04 * SOLAR_MASS),

    'saturn': ([8.34336671824457987e+00,
                4.12479856412430479e+00,
                -4.03523417114321381e-01],
               [-2.76742510726862411e-03 * DAYS_PER_YEAR,
                4.99852801234917238e-03 * DAYS_PER_YEAR,
                2.30417297573763929e-05 * DAYS_PER_YEAR],
               2.85885980666130812e-04 * SOLAR_MASS),

    'uranus': ([1.28943695621391310e+01,
                -1.51111514016986312e+01,
                -2.23307578892655734e-01],
               [2.96460137564761618e-03 * DAYS_PER_YEAR,
                2.37847173959480950e-03 * DAYS_PER_YEAR,
                -2.96589568540237556e-05 * DAYS_PER_YEAR],
               4.36624404335156298e-05 * SOLAR_MASS),

    'neptune': ([1.53796971148509165e+01,
                 -2.59193146099879641e+01,
                 1.79258772950371181e-01],
                [2.68067772490389322e-03 * DAYS_PER_YEAR,
                 1.62824170038242295e-03 * DAYS_PER_YEAR,
                 -9.51592254519715870e-05 * DAYS_PER_YEAR],
                5.15138902046611451e-05 * SOLAR_MASS)}

    return BODIES

# Add iterations
# Add BODIES to parameters
def advance(dt, iterations, BODIES, cached_body_pairs):
    '''
        advance the system one timestep
    '''
    for _ in range(iterations):
        # Remove nested for-loop with cached body pairs
        for body1, body2 in cached_body_pairs:
            ([x1, y1, z1], v1, m1) = BODIES[body1]
            ([x2, y2, z2], v2, m2) = BODIES[body2]

            # Compute deltas
            (dx, dy, dz) = (x1-x2, y1-y2, z1-z2)

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
        
        for body in BODIES.keys():
            (r, [vx, vy, vz], m) = BODIES[body]

            # Update rs
            r[0] += dt * vx
            r[1] += dt * vy
            r[2] += dt * vz

    # Add returned value
    return BODIES
    
# Add BODIES and cached_body_pairs to parameters
def report_energy(BODIES, cached_body_pairs, e=0.0):
    '''
        compute the energy and return it so that it can be printed
    '''
    # Remove nested for-loop with cached body pairs
    for body1, body2 in cached_body_pairs:
        ((x1, y1, z1), v1, m1) = BODIES[body1]
        ((x2, y2, z2), v2, m2) = BODIES[body2]

        # Compute deltas
        (dx, dy, dz) = (x1-x2, y1-y2, z1-z2)

        # Compute energy
        e -= (m1 * m2) / ((dx * dx + dy * dy + dz * dz) ** 0.5)
        
    for body in BODIES.keys():
        (r, [vx, vy, vz], m) = BODIES[body]
        e += m * (vx * vx + vy * vy + vz * vz) / 2.
        
    return e

# Add BODIES to parameters
def offset_momentum(ref, BODIES, px=0.0, py=0.0, pz=0.0):
    '''
        ref is the body in the center of the system
        offset values from this reference
    '''
    for body in BODIES.keys():
        (r, [vx, vy, vz], m) = BODIES[body]
        px -= vx * m
        py -= vy * m
        pz -= vz * m
        
    (r, v, m) = ref
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m

    # Add returned value
    return BODIES

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
    cached_body_pairs = list(combinations(BODIES.keys(), 2))

    # Add BODIES to parameters
    offset_momentum(BODIES[reference], BODIES)

    for _ in range(loops):
        # Move loop into advance()
        BODIES = advance(0.01, iterations, BODIES, cached_body_pairs)
        print(report_energy(BODIES, cached_body_pairs))

if __name__ == '__main__':

    # Compute total runtime for 1 run
    import timeit
    print(timeit.timeit("nbody(100, 'sun', 20000)", setup="from __main__ import nbody", number=1))
