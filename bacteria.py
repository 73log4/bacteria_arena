import itertools
from utils import *
import random
import math


class Bacteria:

    def __init__(self, bacteria_id='', name="Anonymous"):
        self.name = name
        self.decision_map = {s : -1 for s in POSSIBLE_STATES}
        self.decision_map.update({"OOOO" : 1})
        self.decision_map.update({"".join(s): 0 for s in itertools.product("_X", repeat=4)})
        if bacteria_id != '':
            self.set_decision_map_by_bacteria_id(bacteria_id)

    def __getitem__(self, state):
        return self.decision_map[state]

    def __str__(self):
        return f'[Bacteria object: name = {self.name}, id = {self.get_bacteria_id()}]'

    def get_bacteria_id(self):
        strategy_id = ""
        if not self.is_initialized():
            print('Error is Bacteria.get_bacteria_id: bacteria is not fully initialized, hence has no id')
        for s in POSSIBLE_STATES:
            strategy_id += str(self[s])
        return hex(int(strategy_id, 2))[2:]

    def get_color(self):
        bacteria_id = self.get_bacteria_id()
        a = int(bacteria_id, 16)
        r, g, b = math.sin(a % 71), math.sin(a % 71 - 1), math.sin(a % 71 - 2)
        return round(r * 10000) % 255, round(g * 10000) % 255, round(b * 10000) % 255


    def set_decision(self, state, result):
        self.decision_map[state] = result

    def set_decision_map_by_bacteria_id(self, b_id):
        binary_id = bin(int(b_id, 16))[2:].zfill(65)
        for b, s in zip(binary_id, POSSIBLE_STATES):
            self.decision_map[s] = int(b)

    def set_random_decision_map(self):
        for t in STATE_TYPE_DICT:
            if t not in TRIVIAL_STATE_TYPES:
                total_type_cnt = len(STATE_TYPE_DICT[t])
                cell_type_cnt = 0
                for s in STATE_TYPE_DICT[t]:
                    if self.decision_map[s] == 1:
                        cell_type_cnt += 1
                unassigned_states = [s for s in STATE_TYPE_DICT[t] if self.decision_map[s] == -1]
                num_new_states = (total_type_cnt // 2) - cell_type_cnt
                if num_new_states < 0:
                    print(f"Error: bacteria contains more than half positive states of type {t}")
                    return
                random_new_states = random.sample(unassigned_states, k=num_new_states)
                for s in unassigned_states:
                    if s in random_new_states:
                        self.set_decision(s, 1)
                    else:
                        self.set_decision(s, 0)

    def small_random_change(self):
        positive_states = [s for s in POSSIBLE_STATES if s != 'OOOO' and self[s] == 1]
        change_state_1 = random.choice(positive_states)
        state_type = get_state_type(change_state_1)
        negative_states = [s for s in STATE_TYPE_DICT[state_type] if self[s] == 0]
        change_state_2 = random.choice(negative_states)
        self.set_decision(change_state_1, 0)
        self.set_decision(change_state_2, 1)

    def random_change(self, n):
        for i in range(n):
            self.small_random_change()

    def clear_decision_map(self):
        self.decision_map = {s: -1 for s in POSSIBLE_STATES}
        self.decision_map.update({"OOOO": 1})

    def is_legal(self):
        if not self.is_initialized():
            return False
        for t in STATE_TYPE_DICT:
            if t != (0, 4, 0):
                negative_states = [s for s in STATE_TYPE_DICT[t] if self[s] == 0]
                positive_states = [s for s in STATE_TYPE_DICT[t] if self[s] == 1]
                if len(positive_states) > len(negative_states):
                    return False
        for s in ENEMY_STATES:
            if self[s] == 1:
                return False
        return True

    def is_initialized(self):
        return all([self[s] != -1 for s in POSSIBLE_STATES])
