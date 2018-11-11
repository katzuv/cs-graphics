from minesweeper import Board, Cell


def test_surrounding_cells():
    board = Board()
    assert set(board.surrounding_cells(Cell(2, 3, board))) == {(1, 2), (1, 3), (1, 4), (2, 2), (2, 4), (3, 2), (3, 3),
                                                               (3, 4)}
    assert set(board.surrounding_cells(Cell(0, 0, board))) == {(0, 1), (1, 0), (1, 1)}
    assert set(board.surrounding_cells(Cell(1, 0, board))) == {(0, 0), (0, 1), (1, 1), (2, 1), (2, 0)}
