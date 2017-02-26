"""
    Generating binary strings.
"""
from itertools import combinations


def zbits(n, k):
    '''
    Generate a set of all binary strings of length n that contain k zero bits.

    Args:
        n - length of binary strings
        k - number of zeros

    Return:
        result - a set of all such binary strings
    '''
    # Raise exception if k or n is not an int or even not a number
    try:
        # If k or n is not an int
        if int(k) != k or int(n) != n:
            raise ValueError("k and n must be int")
    except:
        # If k or n can not be converted to int
        raise ValueError("k and n must be int")
    else:
        # Raise exception if n<=0
        if n <= 0:
            raise ValueError("n must be greater than 0")

        # Raise exception if k<0
        if k < 0:
            raise ValueError("k must be greater than or equal to 0")

        # Raise exception if k>n
        if k > n:
            raise ValueError("k must be less than or equal to n")

        # Initialize the result set
        result = set()

        # Initialize all indeces of length n
        all_indices = range(n)

        # Use itertools.combinations to generate all combinations of indices of '0' and let others be '1'
        for indices_of_zeros in combinations(all_indices, k):
            # Generate a list of '0' and '1' according to indices_of_zeros
            # Use ''.join() to convert it into a string
            result.add(''.join(['0' if x in indices_of_zeros else '1' for x in all_indices]))

        return result


def print_zbits(n, k):
    '''
    Print all binary strings of length n that contain k zero bits, one per line.

    Args:
        n - length of binary strings
        k - number of zeros

    Return:
        none
    '''
    for item in zbits(n, k):
        print(item)


def main():
    # Provided test cases
    assert zbits(4, 3) == {'0100', '0001', '0010', '1000'}
    assert zbits(4, 1) == {'0111', '1011', '1101', '1110'}
    assert zbits(5, 4) == {'00001', '00100', '01000', '10000', '00010'}

if __name__ == '__main__':
    main()