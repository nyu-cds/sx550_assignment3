from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Initialize a numpy array of length 1 as buffer
num = np.ones(1, dtype=int)

# Raise exception if no enough processes
if size < 2:
    raise ValueError('Need at least 2 processes')

# If the first process
if rank == 0:
    get_valid_input = False
    while not get_valid_input:
        # Check if input is an integer
        try:
            temp = int(input('Input a number for process 0: '))
        except ValueError as err:
            print('Input must be an integer')
            continue

        # Check if input is less than 100
        if temp >= 100:
            print('Input number must be less than 100')
        # Set flag to True in order to stop while-loop
        else:
            get_valid_input = True
    # Save input to buffer
    num *= temp
    comm.Send(num, dest=1)
    comm.Recv(num, source=size-1)
    print(num[0])

# If not the last or the first process
# Multiply by its rank and send to next process
elif rank == size-1:
    comm.Recv(num, source=rank-1)
    num *= rank
    comm.Send(num, dest=0)

# If the last process
# Multiply by its rank and send to process 0
else:
    comm.Recv(num, source=rank-1)
    num *= rank
    comm.Send(num, dest=rank+1)
