from pyspark import SparkContext
from operator import add
from math import sqrt

if __name__ == '__main__':
    sc = SparkContext("local", "meansqrt")
    # Create an RDD of numbers from 1 to 1,000
    nums = sc.parallelize(range(1,1001))
    # Compute the square root of each element using map()
    sqrts = nums.map(sqrt)
    # Compute the sum of square roots using fold(),
    # and then compute the average.
    result = sqrts.fold(0, add) / 1000
    print(result)
