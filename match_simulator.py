from game_arena import Arena
from bacteria import Bacteria
from board_generation import generate_board
from settings import *
from utils import *
import random
import copy
import math


def run_fast_match(bacteria_1, bacteria_2, board):
    """"
    runs a match between two bacterias on input board.
    returns 0 if bacteria_1 won, and 1 if bacteria_2 won
    :param board: board to play match on - must be of appropriate form
    :param bacteria_1: Bacteria object of first bacteria
    :param bacteria_2: Bacteria object of second bacteria
    :return: 0 if bacteria_1 won, 1 if bacteria_2 won
    """
    arena = Arena(bacteria_1, bacteria_2, board)
    for i in range(MATCH_LENGTH):
        bacterias_cnt = arena.count_cells()
        in_game = [b for b in range(len(bacterias_cnt)) if bacterias_cnt[b] > 0]
        if len(in_game) == 1:  # checks if only one bacteria is present in arena, i.e. it won
            return in_game[0]
        arena.run_iteration()
    winner = largest_bacteria(arena.count_cells())  # check which bacteria has more cells in arena
    return winner


def run_match(bacteria_1, bacteria_2):
    """
    runs a match between two bacterias on random board. generating random board may be slow,
    so for running large number of matches run_fast_match with the same pre-generated board is recommended.
    returns 0 if bacteria_1 won, and 1 if bacteria_2 won
    :param bacteria_1: Bacteria object of first bacteria
    :param bacteria_2: Bacteria object of second bacteria
    :return: 0 if bacteria_1 won, 1 if bacteria_2 won
    """
    return run_fast_match(bacteria_1, bacteria_2, generate_board())


def improve_bacteria(bacteria_id, step, games):
    """
    Performs random 'swaps' in the bacteria decision map until it finds a set of swaps that win
    the original bacteria in more that half of the games. A 'swap' is turning one positive
    state to negative and another negative state to positive. The states are of the same type
    :param bacteria_id: id of bacteria to be improved
    :param step: number of random 'swaps' of states
    :param games: number of games to play between old bacteria and new one to check if it is better
    :return: id of improved bacteria
    """
    bacteria_1 = Bacteria(bacteria_id=bacteria_id)
    bacteria_2 = Bacteria(bacteria_id=bacteria_id)
    while True:
        bacteria_2.random_change(step)  # performs swaps
        wins = 0  # number of wins of the new bacteria
        for i in range(games):
            if run_match(bacteria_1, bacteria_2) == 1:
                wins += 1
        if wins > games / 2:
            return bacteria_2.get_bacteria_id()
        bacteria_2.set_decision_map_by_bacteria_id(bacteria_id)  # new bacteria is not better, return to original one


def compare_bacterias(bacteria_1, bacteria_2, games):
    """
    Plays a number of games between two bacterias and returns the number of wins of each one
    :param bacteria_1: bacteria object of first bacteria
    :param bacteria_2: bacteria object of second bacteria
    :param games: number of games to be played
    :return: return a tuple of length 2, first value is number of wins of bacteria_1,
    and second value is number of wins of bacteria 2
    """
    bacteria_1_wins = 0
    for i in range(games):
        if run_match(bacteria_1, bacteria_2) == 0:
            bacteria_1_wins += 1
    return bacteria_1_wins, games - bacteria_1_wins


def run_competition(bacterias, games, details=False):
    """
    runs a competition where every bacteria plays 2*games matches with random opponents.
    if details=True returns a NxN (N=number of bacterias) list, where:
    list[i][j] = 1 - if bacteria i won bacteria j
    list[i][j] = 0 - if bacteria i lost to bacteria j
    list[i][j] = -1 - if no match was played between bacteria i and bacteria j
    if details=False returns a list of the bacterias indexes sorted by the
    best bacteria in the competition to the worst (so list[0] is the index of the bacteria which won the most times)
    :param bacterias: list of Bacteria objects
    :param games: number of games to be played (every bacteria will actually play twice this number of games)
    :param details: indicates if a detailed competition graph should be returned or just the final results
    :return: see explanation above
    """
    bacterias = copy.copy(bacterias)  # to not change original list
    random.shuffle(bacterias)  # determines the matches

    n = len(bacterias)
    results = [[-1 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(1, games + 1):
            k = (i + j) % n  # opponent of bacteria i
            if i != k and results[i][k] == -1:  # check if match was not already played and if opponent is not itself
                match_result = run_match(bacterias[k], bacterias[i])
                results[i][k] = match_result
                results[k][i] = (match_result + 1) % 2  # switch 0 and 1

    if not details:
        wins = [len([a for a in results[i] if a == 1]) for i in range(n)]
        return sorted(list(range(n)), key=lambda i: wins[i], reverse=True)
    return results


def run_tournament(bacterias, details=False):
    """
    runs a competition where every bacteria plays with every other bacteria
    """
    return run_competition(bacterias, len(bacterias) - 1, details=details)


def run_pyramid_competition(bacterias):
    """
    run a pyramid style competition with bacterias list. the list must have a length that is a power of 2.
    returns a list of the bacterias ordered by there final standings in the competition (so element 0 is the winner)
    :param bacterias: list of Bacteria objects
    :return: bacterias list ordered by there final standings
    """
    standings = []
    if not math.log(len(bacterias), 2).is_integer():
        exit('Error in run_pyramid_competition: length of bacterias list must be a power of 2')

    new_bacterias, old_bacterias = [], bacterias
    while len(old_bacterias) != 1:
        for i in range(0, len(old_bacterias), 2):
            b1, b2 = old_bacterias[i], old_bacterias[i + 1]
            if run_match(b1, b2) == 0:  # b1 won
                standings.append(b2)
                new_bacterias.append(b1)
            else:  # b2 won
                standings.append(b1)
                new_bacterias.append(b2)
        new_bacterias, old_bacterias = [], new_bacterias

    standings.append(old_bacterias[0])  # append winner
    standings.reverse()
    return standings


