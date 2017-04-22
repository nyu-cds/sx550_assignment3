'''
Test script for parallel sorter.
To run test: mpiexec -n N python test.py
where N is an integer greater than 1.
'''

import unittest
from parallel_sorter import psort, slice_data, LENGTH
from mpi4py import MPI
import numpy as np

class TestSorter(unittest.TestCase):

    def setUp(self):
        comm = MPI.COMM_WORLD
        self.rank = comm.Get_rank()

    def test_slice_data(self):
        '''
        Sliced data should be a list of 'size' lists:
            The first list should only contains the minimal number (maybe repeated), which will be kept in process 0.
            Other lists should contains data which will be sent to other process.
        '''
        if self.rank == 0:
            data = [2,1,1,3,5,4]
            result = [[1,1],[2,3],[5,4]]
            sliced_data = slice_data(data, 3)
            for i in range(len(result)):
                self.assertTrue(np.array_equal(result[i], sliced_data[i]))
        else:
            pass

    def test_psort(self):
        '''
        For process 0, check whether results are sorted correctly.
        For other process, check whether their results are None.
        '''
        result = psort()
        if self.rank == 0:
            self.assertEqual(sorted(result), result)
            self.assertEqual(len(result), LENGTH)
        else:
            self.assertEqual(None, result)

if __name__ == '__main__':
    unittest.main()
