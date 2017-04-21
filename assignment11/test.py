'''
Test script for parallel sorter.
To run test: mpiexec -n N python test.py
where N is an integer greater than 1.
'''

import unittest
from parallel_sorter import psort
from mpi4py import MPI

class TestSorter(unittest.TestCase):

    def test_sort(self):
        '''
        For process 0, check whether results are sorted correctly.
        For other process, check whether their results are None.
        '''
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        result = psort()
        if rank == 0:
            self.assertEqual(sorted(result), result)
        else:
            self.assertEqual(None, result)

if __name__ == '__main__':
    unittest.main()
