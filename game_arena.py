from settings import *
from utils import *
import copy


class Arena:

    def __init__(self, bacteria_1, bacteria_2, start_board):
        self.bacteria_1 = bacteria_1
        self.bacteria_2 = bacteria_2
        self.bacterias = [bacteria_1, bacteria_2]

        self.board = copy.copy(start_board)
        self.non_wall_coordinates = [c for c in BOARD_COORDINATES if self.board[c] != WALL]

        self.bacteria_colors = [self.bacteria_1.get_color(), self.bacteria_2.get_color()]

        self.neighbors = {}
        self.set_neighbors()

    def count_cells(self):
        cnt_list = [0, 0]
        for c in BOARD_COORDINATES:
            cell = self.board[c]
            if cell >= 0:
                cnt_list[cell] += 1
        return cnt_list

    def set_neighbors(self):
        for c in BOARD_COORDINATES:
            self.neighbors[c] = [(c[0] + i, c[1] + j) for i, j in DIRECTIONS]

    def get_coordinate_neighbor_state(self, c, player):
        order = ORDER[player]
        state = ''
        for i in order:
            cell = self.board[self.neighbors[c][i]]
            if cell < 0:
                state += '_'
            elif cell == player:
                state += 'O'
            else:
                state += 'X'
        return state

    def run_iteration(self):
        new_board = copy.copy(self.board)
        for c in self.non_wall_coordinates:
            state_1, state_2 = self.get_coordinate_neighbor_state(c, 0), self.get_coordinate_neighbor_state(c, 1)
            update_1, update_2 = self.bacteria_1[state_1], self.bacteria_2[state_2]

            if update_1 == 1 and update_2 == 0:
                new_board[c] = 0
            elif update_1 == 0 and update_2 == 1:
                new_board[c] = 1
            elif update_1 == update_2 == 0:
                new_board[c] = EMPTY


        self.board = new_board
