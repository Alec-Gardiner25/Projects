import sys
import numpy as np
import pygame
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):

    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT-1,-1,-1):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check all horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if all(x == piece for x in board[r][c:c+4]):
                return True

    #Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT,3,-1):
            if all(x == piece for x in board[:,c][r-4:r]):
                return True

    # Check positive sloped Diagonal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT,3,-1):
            if all(x == piece for x in np.diag(np.fliplr(board[:,c:c+4][r-4:r]))):
                return True

    # check negatively sloped diagonals
    for c in range(COLUMN_COUNT,3,-1):
        for r in range(ROW_COUNT,3,-1):
            if all(x == piece for x in np.diag(board[:,c-4:c][r-4:r])):
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(window, BLUE, (c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE, SQUARESIZE,SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(window, BLACK,
                                   (c * SQUARESIZE + int(SQUARESIZE / 2), r * SQUARESIZE + int(3 * SQUARESIZE / 2)),
                                   RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(window, RED,
                                   (c * SQUARESIZE + int(SQUARESIZE / 2), r * SQUARESIZE + int(3 * SQUARESIZE / 2)),
                                   RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(window, YELLOW,
                                   (c * SQUARESIZE + int(SQUARESIZE / 2), r * SQUARESIZE + int(3 * SQUARESIZE / 2)),
                                   RADIUS)
    pygame.display.update()


board = create_board()

game_over = False

turn = 0

winner = "Nobody"

pygame.init()

width = COLUMN_COUNT * SQUARESIZE

height = (ROW_COUNT+1) * SQUARESIZE

size = (width,height)

window = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(window, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn % 2 == 0:
                pygame.draw.circle(window, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(window, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event.pos)
            # Ask for p1 input
            if turn == 0:
                posx = event.pos[0]
                col = posx//SQUARESIZE

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    game_over = winning_move(board,1)
                    if game_over:
                        pygame.draw.rect(window, BLACK, (0, 0, width, SQUARESIZE))
                        label = font.render("Player 1 wins!", 1, RED)
                        window.blit(label,(40,10))
                else:
                    print("Invalid location, Try again")
                    turn -= 1
            # Ask for p2 input
            else:
                posx = event.pos[0]
                col = posx//SQUARESIZE

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    game_over = winning_move(board,2)
                    if game_over:
                        pygame.draw.rect(window, BLACK, (0, 0, width, SQUARESIZE))
                        label = font.render("Player 2 wins!", 1, YELLOW)
                        window.blit(label,(40,10))

                else:
                    print("Invalid location, Try again")
                    turn -= 1
            draw_board(board)
            turn += 1
            turn %= 2
            if game_over:
                pygame.time.wait(2000)
