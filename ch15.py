__author__ = 'Kiran'
import sys
INFINITY = sys.maxint


def print_neatly(words, M):
    """
    :param words: the list of words the that has to be printed neatly.
    :param M: The maximum width of each line.
    :return: the cost and the text that can be printed neatly.
    >>> words = ['solution', 'for', 'coding', 'assignment', 'print', 'neatly', 'with', 'DP' ]
    >>> M = 10
    >>> print_neatly(words, M)
    (197, 'solution\\nfor coding\\nassignment\\nprint\\nneatly\\nwith DP')
    """
    n = len(words)

    spaces = [[int(INFINITY) for i in range(n)] for j in range(n)]
    cost = [0 for i in range(n)]
    parent = [0 for i in range(n)]

    for i in range(n):
        spaces[i][i] = M - len(words[i])
        for j in range(i + 1, n):
            spaces[i][j] = spaces[i][j - 1] - len(words[j]) - 1

    spaces = __calc_spaces(spaces, n)

    for i in range(n - 1, -1, -1):
        cost[i] = spaces[i][n - 1]
        parent[i] = n
        for j in range(n - 1, i, -1):
            if spaces[i][j - 1] == INFINITY:
                continue
            if cost[j] + spaces[i][j - 1] < cost[i]:
                cost[i] = cost[j] + spaces[i][j - 1]
                parent[i] = j

    word = __print_text(words, parent)

    return cost[0], word[:-1]


def __calc_spaces(spaces, n):
    for i in range(n):
        for j in range(i, n):
            if spaces[i][j] < 0:
                spaces[i][j] = INFINITY
            elif j == n - 1 and spaces[i][j] >= 0:
                spaces[i][j] = 0
            else:
                spaces[i][j] **= 3
    return spaces


def __print_text(words, parent):
    word = ""
    i = 0
    while i < (len(parent)):
        limit = parent[i]
        for j in range(i, limit):
            word += words[j] + " "
        word = word[:-1]
        word += "\n"
        i = limit
    return word


if __name__ == '__main__':
    import doctest
    doctest.testmod()
