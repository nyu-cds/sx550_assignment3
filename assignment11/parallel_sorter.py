from mpi4py import MPI
import numpy as np
import itertools

# Length of data
LENGTH = 10000

def slice_data(data, size):
    # Prepare for slicing
    data = np.array(data)
    min_num, max_num = min(data), max(data)
    delta = (max_num - min_num) / (size-1)

    # Process 0 keeps the least number and other processes get range evenly
    data_sliced = [data[(data>min_num+delta*(i-1)) & (data<=min_num+delta*(i))] for i in range(size)]

    return data_sliced

def psort():
    '''
    Funtion for Parallel Sorting.
    '''
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Check number of processes
    if size < 2:
        raise ValueError('You need at least 2 processes')

    # Process 0 generates data and slice it according number of processes
    if rank == 0:
        # Generates random data
        data = np.random.randint(0, LENGTH, LENGTH)
        data_sliced = slice_data(data, size)

    else:
        data_sliced = None

    # Send sliced data to processes
    data_local = comm.scatter(data_sliced, root=0)

    # Sort sliced data
    if rank != 0:
        data_local.sort()

    # Gather sorted data
    result = comm.gather(data_local, root=0)

    # Process 0 flattens gathered data
    if rank == 0:
        result = list(itertools.chain.from_iterable(result))

    return result

if __name__ == '__main__':
    result = psort()
    print(result)
