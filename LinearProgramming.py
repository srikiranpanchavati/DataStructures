# -*- coding: utf-8 -*-
from mprint import printmat

NAME = 'spanchav'


def lu(A):
    """
    >>> A = [[4, -5,  6], [8, -6,  7], [12, -7, 12]]
    >>> lu(A)
    ([[4, -5, 6], [2, 4, -5], [3, 2, 4]], 'solved')
    """
    n = len(A)
    LU = [[A[i][j] for j in range(n)] for i in range(n)]
    for k in range(0, n):
        printmat(LU)
        for i in range(k + 1, n):
            LU[i][k] = LU[i][k] / LU[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                LU[i][j] = LU[i][j] - LU[i][k] * LU[k][j]
        printmat(LU)
    return LU, 'solved'


def lup(A):
    """
    >>> A = [[2,  0,   2, 0.6], [3,  3,   4,  -2], [5,  5,   4,   2], [-1, -2, 3.4,  -1]]
    >>> lup(A)
    ([[5.0, 5.0, 4.0, 2.0], [0.4, -2.0, 0.3999999999999999, -0.20000000000000007], [-0.2, 0.5, 4.0, -0.49999999999999994], [0.6, -0.0, 0.4, -3.0]], [2, 0, 3, 1], 'solved')
    """
    n = len(A)
    LU = [[float(A[i][j]) for j in range(n)] for i in range(n)]
    pi = range(n)

    for k in range(n):
        printmat(LU, perm=pi)
        p = 0
        for i in range(k, n):
            if abs(LU[i][k]) > p:
                p = abs(LU[i][k])
                q = i

        if p == 0:
            raise Exception("Error Singular Matrix")

        temp = pi[k]
        pi[k] = pi[q]
        pi[q] = temp

        temp = LU[k]
        LU[k] = LU[q]
        LU[q] = temp

        for i in range(k + 1, n):
            LU[i][k] /= LU[k][k]
            for j in range(k + 1, n):
                LU[i][j] -= LU[i][k] * LU[k][j]
        printmat(LU, perm=pi)
    return LU, pi, 'solved'


def lupsolve(LU, pi, b):
    """
    >>> LU = [[5.0,  6.0,  3.0], [0.2,  0.8, -0.6], [0.6,  0.5,  2.5]]
    >>> pi = [2, 0, 1]
    >>> b = [3.0, 7.0, 8.0]
    >>> lupsolve(LU, pi, b)
    [-1.4, 2.1999999999999997, 0.6]
    """
    n = len(b)
    x = [float(b[pi[i]]) for i in range(n)]
    y = range(n)
    for i in range(n):
        l_sum = 0
        for j in range(0, i):
            l_sum += LU[i][j] * y[j]
        y[i] = b[pi[i]] - l_sum
    for i in range(n - 1, -1, -1):
        u_sum = 0
        for j in range(i + 1, n):
            u_sum += LU[i][j] * x[j]
        x[i] = (y[i] - u_sum) / LU[i][i]
    return x


def pivot(A, row, col):
    """
    >>> A = [[1, -3, -1, -2, 0, 0, 0,  0], [0, 1, 1, 3, 1, 0, 0,  30], [0, 2, 2, 5, 0, 1, 0,  24], [0, 4, 1, 2, 0, 0, 1,  36]]
    >>> row = 3
    >>> col = 3
    >>> pivot(A, row, col)
    [[1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 36.0], [0.0, -5.0, -0.5, 0.0, 1.0, 0.0, -1.5, -24.0], [0.0, -8.0, -0.5, 0.0, 0.0, 1.0, -2.5, -66.0], [0.0, 2.0, 0.5, 1.0, 0.0, 0.0, 0.5, 18.0]]
    """
    m = len(A)
    n = len(A[0])
    Ahat = [[0] * n for i in range(m)]

    pivot_val = float(A[row][col])
    for i in range(0, n):
        Ahat[row][i] = float(A[row][i]) / pivot_val

    for i in range(0, m):
        if i != row:
            for j in range(0, n):
                Ahat[i][j] = A[i][j] - ((A[i][col] / pivot_val) * float(A[row][j]))
    return Ahat


#
# Do not modify below this point
# This is a freeby -- I will make future semesters implement this....
#
def simplex(A):
    # Assume that the input is already put into a table.
    # Assume that the input is feasible already (no need to check)
    m = len(A)
    n = len(A[0])
    x = [0] * (n - 1)
    wiggle = [0] * m
    while min(A[0][1:-1]) < 0:
        # find entering variable
        col = A[0].index(min(A[0][1:-1]))

        min_wiggle = float('inf')
        row = None
        for i in range(1, m):
            if A[i][col] > 0:
                wiggle = A[i][-1] / float(A[i][col])
            if wiggle < min_wiggle:
                min_wiggle = wiggle
                row = i
        if row is None:
            return A, x, 'unbounded'
        printmat(A, pos=(row, col), row=row, col=col)

        A = pivot(A, row, col)

        printmat(A, pos=(row, col), row=row, col=col)

    # Look for the basic variables and copy into x
    for j in range(0, n - 1):
        colvec = [A[i][j] for i in range(m)]  # copy out the column

        # Check if colvec is a column of the identity matrix.
        if colvec.count(0.0) == m - 1 and colvec.count(1.0) == 1:
            x[j] = A[colvec.index(1)][-1]
        else:
            x[j] = 0

    return A, x, 'solved'


LU_MATRIX = [[4, -5, 6],
             [8, -6, 7],
             [12, -7, 12]]

LUP_MATRIX = [[2, 0, 2, 0.6],
              [3, 3, 4, -2],
              [5, 5, 4, 2],
              [-1, -2, 3.4, -1]]

SIMPLEX_MATRIX = [[1, -3, -1, -2, 0, 0, 0, 0],
                  [0, 1, 1, 3, 1, 0, 0, 30],
                  [0, 2, 2, 5, 0, 1, 0, 24],
                  [0, 4, 1, 2, 0, 0, 1, 36]]

LUPSOLVE_P = [2, 0, 1]
LUPSOLVE_MATRIX = [[5.0, 6.0, 3.0],
                   [0.2, 0.8, -0.6],
                   [0.6, 0.5, 2.5]]
LUPSOLVE_B = [3.0, 7.0, 8.0]


def check_lu():
    A = LU_MATRIX
    print "==========================="
    print "Submitted by ", NAME
    print "LU:"
    print "Input:"
    printmat(A)
    print "Steps:"
    LU, result = lu(A)
    print "---------------------------"
    print "Output:"
    printmat(LU)
    print 'result = ', result
    print "---------------------------"


def check_lup():
    A = LUP_MATRIX
    print "==========================="
    print "Submitted by ", NAME
    print "LUP:"
    print "---------------------------"
    print "Input:"
    printmat(A)
    print "---------------------------"
    print "Steps:"
    LUP, p, result = lup(A)
    print "---------------------------"
    print "Output:"
    printmat(LUP, perm=p)
    print "---------------------------"
    print "result = ", result
    print "---------------------------"


def check_lupsolve():
    pi = LUPSOLVE_P
    LU = LUPSOLVE_MATRIX
    b = LUPSOLVE_B

    print "==========================="
    print "Submitted by ", NAME
    print "LUP-SOLVE:"
    print "---------------------------"
    print "Input:"
    printmat(LU, pi)
    print "RHS:"
    print b
    print "---------------------------"
    x = lupsolve(LU, pi, b)
    print "x = [" + ', '.join(['%3.1f' % z for z in x]) + ']'
    print "---------------------------"


def check_simplex():
    A = SIMPLEX_MATRIX
    print "==========================="
    print "Submitted by ", NAME
    print "SIMPLEX:"
    print "Input:"
    printmat(A)
    print "Steps:"
    SIMP, x, result = simplex(A)
    print "---------------------------"
    print "Output:"
    printmat(SIMP)
    print "result = ", result
    print "     z = ", x[0]
    print "     x = ", x[1:]
    print "---------------------------"


def check_all():
    check_lu()
    check_lup()
    check_simplex()
    check_lupsolve()


if __name__ == '__main__':
    USE_COLORS = True
    check_all()
    import doctest
    print("Doc Test")
    doctest.testmod()
