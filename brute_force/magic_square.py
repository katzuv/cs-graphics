from itertools import permutations
from pprint import pprint


def is_magic_square(square):
    """
    :param square: square to check
    :return: whether :square: is a Magic Square
    """
    total = sum(square[0])

    def is_not_total(cells):
        return sum(cells) != total

    for row in square:
        if is_not_total(row):
            return False

    for column in zip(*square):
        if is_not_total(column):
            return False

    main_diagonal = [square[row][row] for row in xrange(len(square))]
    if is_not_total(main_diagonal):
        return False
    secondary_diagonal = [square[row][len(square) - 1 - row] for row in xrange(len(square))]
    if is_not_total(secondary_diagonal):
        return False

    return True


def squares():
    """
    :return: generator with all the possible 3X3 squares.
    """
    for p in permutations(xrange(1, 10)):
        yield p[:3], p[3:6], p[6:]


def magic_square():
    """
    :return: all squares which are Magic Squares.
    :rtype: list
    """
    solutions = list()
    for square in squares():
        if is_magic_square(square):
            solutions.append(square)
    return solutions


def main():
    """Main function."""
    pprint(magic_square())


if __name__ == '__main__':
    main()
