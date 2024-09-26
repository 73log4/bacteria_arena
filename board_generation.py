import random
from settings import *
from utils import *
import itertools


def generate_board(squares=True):
    board = {c: EMPTY for c in itertools.product(range(-1, BOARD_SIZE + 1), repeat=2)}
    if squares and GENERATE_SQUARES:
        generate_random_squares(board)

    player_1_possible_spawns = [c for c in PLAYER_1_SPAWN_COORDINATES if board[c] != WALL]
    player_2_possible_spawns = [c for c in PLAYER_2_SPAWN_COORDINATES if board[c] != WALL]
    player_1_spawns = random.sample(player_1_possible_spawns, k=INITIAL_SPAWN)
    player_2_spawns = random.sample(player_2_possible_spawns, k=INITIAL_SPAWN)
    for c in player_1_spawns:
        board[c] = 0
    for c in player_2_spawns:
        board[c] = 1
    return board


def generate_random_squares(board):
    above_diagonal = [c for c in BOARD_COORDINATES if c[0] >= c[1]]
    square_cnt = random.randint(0, SQUARE_CNT_RANGE)
    square_start_coordinates = random.sample(above_diagonal, square_cnt)
    for c in square_start_coordinates:
        square_length = random.randint(1, SQUARE_SIZE_RANGE)
        square_coordinates = []
        delete_square = False
        for i in range(square_length):
            for j in range(square_length):
                new_c = c[0] + i, c[1] + j
                if new_c in above_diagonal:
                    if board[new_c] == WALL:
                        delete_square = True
                    else:
                        square_coordinates.append(new_c)
                elif new_c in BOARD_COORDINATES:
                    delete_square = True
        if not delete_square:
            for c2 in square_coordinates:
                board[c2] = WALL
    for c in above_diagonal:
        board[c[1], c[0]] = board[c]
