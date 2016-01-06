# -*- coding: utf-8 -*-
from numpy import *  # analysis:ignore
from sys import *

# STOCK_PRICES  = [100,113,110,85,105,102,86,63,81,101,94,106,101,79,94,90,97]
STOCK_PRICE_CHANGES = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
matrix1 = [[1, 2, 3, 4], [5, 6, 7, 8], [3, 4, 5, 6], [8, 9, 1, 2]]
matrix2 = [[9, 10, 11, 12], [13, 14, 15, 16], [2, 4, 6, 8], [3, 5, 7, 9]]


# Implement pseudo-code from the book
def find_maximum_subarray_brute(A, low=0, high=-1):
    """
     >>> STOCK_PRICE_CHANGES = [13,-3,-25,20,-3,-16,-23,18,20,-7,12,-5,-22,15,-4,7]
     >>> find_maximum_subarray_brute(STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES) - 1)
     (7, 10)

     >>> STOCK_PRICE_CHANGES = [100,113,110,85,105,102,86,63,81,101,94,106,101,79,94,90,97]
     >>> find_maximum_subarray_brute(STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES) - 1)
     (0, 16)

     >>> STOCK_PRICE_CHANGES = [-3, -4, -1, -2]
     >>> find_maximum_subarray_brute(STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES) - 1)
     (2, 2)
    """

    max_sum = -maxint - 1
    for i in range(len(A)):
        cur_sum = 0
        for j in range(i, len(A)):
            cur_sum += A[j]
            if cur_sum > max_sum:
                max_sum = cur_sum
                low = i
                high = j
    return low, high


# Implement pseudo-code from the book
def find_maximum_crossing_subarray(A, low, mid, high):
    """
    Find the maximum sub-array that crosses mid
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    """
    left_max = A[mid]
    right_max = A[mid + 1]
    sum_left = sum_right = 0
    left_index = mid
    right_index = mid + 1
    for i in range(mid, low - 1, -1):
        sum_left += A[i]
        if sum_left > left_max:
            left_max = sum_left
            left_index = i
    for j in range(mid + 1, high + 1):
        sum_right += A[j]
        if sum_right > right_max:
            right_max = sum_right
            right_index = j
    return left_index, right_index, left_max + right_max


def find_maximum_subarray_recursive(A, low, high):
    """
    >>> STOCK_PRICE_CHANGES = [13,-3,-25,20,-3,-16,-23,18,20,-7,12,-5,-22,15,-4,7]
    >>> find_maximum_subarray_recursive(STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES) - 1)
    (7, 10, 43)

    >>> STOCK_PRICE_CHANGES = [100,113,110,85,105,102,86,63,81,101,94,106,101,79,94,90,97]
    >>> find_maximum_subarray_recursive(STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES) - 1)
    (0, 16, 1607)

     >>> STOCK_PRICE_CHANGES = [-3, -4, -1, -2]
    >>> find_maximum_subarray_recursive(STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES) - 1)
    (2, 2, -1)
    """
    if low == high:
        return low, high, A[low]
    else:
        mid = (low + high) / 2
        left_tuple = find_maximum_subarray_recursive(A, low, mid)
        right_tuple = find_maximum_subarray_recursive(A, mid + 1, high)
        cross_tuple = find_maximum_crossing_subarray(A, low, mid, high)
        if (left_tuple[2] >= right_tuple[2]) & (left_tuple[2] >= cross_tuple[2]):
            return left_tuple
        elif (right_tuple[2] >= left_tuple[2]) & (right_tuple[2] >= cross_tuple[2]):
            return right_tuple
        else:
            return cross_tuple


def find_maximum_subarray_iterative(A, low=0, high=-1):
    """
     >>> STOCK_PRICE_CHANGES = [13,-3,-25,20,-3,-16,-23,18,20,-7,12,-5,-22,15,-4,7]
     >>> find_maximum_subarray_iterative(STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES) - 1)
     (7, 10)

     >>> STOCK_PRICE_CHANGES = [100,113,110,85,105,102,86,63,81,101,94,106,101,79,94,90,97]
     >>> find_maximum_subarray_iterative(STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES) - 1)
     (0, 16)

     >>> STOCK_PRICE_CHANGES = [-3, -4, -1, -2]
     >>> find_maximum_subarray_iterative(STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES) - 1)
     (2, 2)

    """
    maxsofar = 0
    maxendinghere = 0
    new_start = low
    for i in range(len(A)):
        maxendinghere = max(maxendinghere + A[i], 0)
        if maxendinghere == 0:
            new_start = i + 1
        maxsofar = max(maxsofar, maxendinghere)
        if maxsofar == maxendinghere & maxsofar != 0:
            high = i
            low = new_start
    if maxsofar == 0:
        for i in range(len(A)):
            if A[i] == max(A):
                return i, i
    return low, high


def square_matrix_multiply(A, B):
    """
    Return the product AB of matrix multiplication.
    >>> matrix1 = [[1, 2, 3, 4], [5, 6, 7, 8], [3, 4, 5, 6], [8, 9, 1, 2]]
    >>> matrix2 = [[9, 10, 11, 12], [13, 14, 15, 16], [2, 4, 6, 8], [3, 5, 7, 9]]
    >>> square_matrix_multiply(matrix1, matrix2)
    [[53, 70, 87, 104], [161, 202, 243, 284], [107, 136, 165, 194], [197, 220, 243, 266]]
    """
    C = [[0 for i in range(len(matrix1))] for j in range(len(matrix2[0]))]
    A = asarray(A)
    B = asarray(B)
    assert A.shape == B.T.shape
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(A[0])):
                C[i][j] += A[i][k] * B[k][j]
    return C


def square_matrix_multiply_strassens(A, B):
    """
    >>> matrix1 = [[1, 2, 3, 4], [5, 6, 7, 8], [3, 4, 5, 6], [8, 9, 1, 2]]
    >>> matrix2 = [[9, 10, 11, 12], [13, 14, 15, 16], [2, 4, 6, 8], [3, 5, 7, 9]]
    >>> square_matrix_multiply(matrix1, matrix2)
    [[53, 70, 87, 104], [161, 202, 243, 284], [107, 136, 165, 194], [197, 220, 243, 266]]
    """
    A = asarray(A)
    B = asarray(B)
    assert (len(A) & (len(A) - 1)) == 0, "A is not a power of 2"
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]
    else:
        n /= 2
        a11, a12, a21, a22 = split_matrix(A, n)
        b11, b12, b21, b22 = split_matrix(B, n)

        s1 = add_sub_matrix(b12, b22, 'sub')
        p1 = square_matrix_multiply_strassens(a11, s1)

        s2 = add_sub_matrix(a11, a12, 'add')
        p2 = square_matrix_multiply_strassens(s2, b22)

        s3 = add_sub_matrix(a21, a22, 'add')
        p3 = square_matrix_multiply_strassens(s3, b11)

        s4 = add_sub_matrix(b21, b11, 'sub')
        p4 = square_matrix_multiply_strassens(a22, s4)

        s5 = add_sub_matrix(a11, a22, 'add')
        s6 = add_sub_matrix(b11, b22, 'add')
        p5 = square_matrix_multiply_strassens(s5, s6)

        s7 = add_sub_matrix(a12, a22, 'sub')
        s8 = add_sub_matrix(b21, b22, 'add')
        p6 = square_matrix_multiply_strassens(s7, s8)

        s9 = add_sub_matrix(a11, a21, 'sub')
        s10 = add_sub_matrix(b11, b12, 'add')
        p7 = square_matrix_multiply_strassens(s9, s10)

        a_sum_diff = add_sub_matrix(p5, p4, 'add')
        b_sum_diff = add_sub_matrix(a_sum_diff, p6, 'add')
        c11 = add_sub_matrix(b_sum_diff, p2, 'sub')
        c12 = add_sub_matrix(p1, p2, 'add')
        c21 = add_sub_matrix(p3, p4, 'add')
        a_sum_diff = add_sub_matrix(p5, p1, 'add')
        b_sum_diff = add_sub_matrix(p3, p7, 'add')
        c22 = add_sub_matrix(a_sum_diff, b_sum_diff, 'sub')

        C = [[0 for k in range(len(matrix1))] for m in range(len(matrix2[0]))]
        for i in range(n):
            for j in range(n):
                C[i][j] = c11[i][j]
                C[i][n + j] = c12[i][j]
                C[n + i][j] = c21[i][j]
                C[n + i][n + j] = c22[i][j]
    return C


def split_matrix(B, n):
    r11 = [[0 for i in range(n)] for j in range(n)]
    r12 = [[0 for i in range(n)] for j in range(n)]
    r21 = [[0 for i in range(n)] for j in range(n)]
    r22 = [[0 for i in range(n)] for j in range(n)]

    for i in range(n):
        for j in range(n):
            r11[i][j] = B[i][j]
            r12[i][j] = B[i][n + j]
            r21[i][j] = B[n + i][j]
            r22[i][j] = B[n + i][n + j]
    return r11, r12, r21, r22


def add_sub_matrix(a, b, op):
    result = [[0 for i in range(len(a))] for j in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a)):
            if op == 'add':
                result[i][j] = a[i][j] + b[i][j]
            else:
                result[i][j] = a[i][j] - b[i][j]
    return result


def test():

    print "Max sub array using brute force: " + str(find_maximum_subarray_brute(STOCK_PRICE_CHANGES))
    print "Max sub array using recursion: " + str(find_maximum_subarray_recursive(STOCK_PRICE_CHANGES, low=0, high=len(STOCK_PRICE_CHANGES) - 1))
    print "Max sub array using iterative method: " + str(find_maximum_subarray_iterative(STOCK_PRICE_CHANGES))
    print "Matrix multiplication: " + str(square_matrix_multiply(matrix1, matrix2))
    print "matrix multiplication strassens' method: " + str(square_matrix_multiply_strassens(matrix1, matrix2))


if __name__ == '__main__':
    test()
    import doctest
    doctest.testmod()

