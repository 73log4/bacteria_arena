import itertools
from settings import BOARD_SIZE, SCREEN_SIZE


TRIVIAL_STATE_TYPES = {(4, 0, 0), (0, 4, 0), (0, 0, 4)}

STATE_TYPE_DICT = {}
for a in range(5):
    for b in range(1, 5 - a):
        c = 4 - a - b
        STATE_TYPE_DICT[(a, b, c)] = []

for s in itertools.product("_OX", repeat=4):
    a, b, c = s.count("_"), s.count("O"), s.count("X")
    if b > 0:
        STATE_TYPE_DICT[(a, b, c)].append("".join(s))

POSSIBLE_STATES = ["".join(s) for s in itertools.product("_OX", repeat=4) if 'O' in s]
ENEMY_STATES = ["".join(s) for s in itertools.product("_X", repeat=4)]

def get_state_type(state):
    return state.count("_"), state.count("O"), state.count("X")

RED_TYPE_TO_STATE_DICT = {'_' : '_', 'R': 'O', 'B': 'X'}
BLUE_TYPE_TO_STATE_DICT = {'_' : '_', 'R': 'X', 'B': 'O'}


ORDER = [[0, 1, 2, 3], [2, 3, 0, 1]]


def largest_bacteria(bacteria_cnt):
    m = max(bacteria_cnt)
    return bacteria_cnt.index(m)


BOARD_COORDINATES = [c for c in itertools.product(range(BOARD_SIZE), repeat=2)]
DIRECTIONS = [(1, 0), (0, -1), (-1, 0), (0, 1)]  # order is important!
DIRECTIONS_STATE_ORDER = {1: [0, 1, 2, 3], 2: [1, 2, 3, 0], 3: [2, 3, 0, 1], 4: [3, 0, 1, 2]}


EMPTY = -1
WALL = -2


PLAYER_1_SPAWN_COORDINATES = [c for c in BOARD_COORDINATES if c[0] + BOARD_SIZE // 3 < c[1]]
PLAYER_2_SPAWN_COORDINATES = [c for c in BOARD_COORDINATES if c[0] > c[1] + BOARD_SIZE // 3]


SCREEN_DIMENSIONS = [SCREEN_SIZE, SCREEN_SIZE]  # must be square
STATUS_BAR_SIZE = 15
STATUS_BAR_SEPARATOR_SIZE = 10
STATUS_BAR_SEPARATOR_COLOR = (255, 255, 255)
SCREEN_DIMENSIONS[1] += STATUS_BAR_SIZE
SQUARE_SIZE = SCREEN_DIMENSIONS[0] // BOARD_SIZE


SQUARE_CNT_RANGE = 8
SQUARE_SIZE_RANGE = 18
