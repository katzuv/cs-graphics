from itertools import product


def check_board(board):
    for row in board:
        if row.count(True) > 1:
            return False
    for column in zip(*board):
        if column.count(True) > 1:
            return False
    queens_cells = [(row, column) for row, column in product(xrange(len(board)), xrange(len(board))) if
                    board[row][column]]
    for first, second in product(queens_cells, queens_cells):
        if first == second:
            continue
        if abs(first[0] - second[0]) == abs(first[1] - second[1]):
            return False
    return True


def queens(board, row=0):
    if row == len(board):
        return True
    for column in xrange(len(board[row])):
        board[row][column] = True
        if check_board(board):
            if queens(board, row + 1):
                return True
        board[row][column] = False
    return False


def print_queens(board):
    for row in board:
        for cell in row:
            if cell:
                print 'Q',
            else:
                print '-',
        print


def main():
    size = 8
    board = [[False for _ in xrange(size)] for _ in xrange(size)]
    if queens(board):
        print_queens(board)
    else:
        print 'No solution'


if __name__ == '__main__':
    main()
