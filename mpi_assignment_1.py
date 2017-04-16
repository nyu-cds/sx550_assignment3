from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Print according to rank
if rank % 2 == 0:
    print("Hello from process", rank)
else:
    print("Goodbye from process", rank)