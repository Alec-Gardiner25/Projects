import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
def create_board():
    board = np.zeros((6,7))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):

    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT-1,-1,-1):
        if board[r][col] == 0:
            return r


board = create_board()

game_over = False

turn = 0

while not game_over:
    # Ask for p1 input
    print(board)
    if turn == 0:
        col = int(input("Player 1, make your Selection (0-6): "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

    # Ask for p2 input
    else:
        col = int(input("Player 2, make your Selection (0-6): "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

    turn += 1
    turn %= 2

