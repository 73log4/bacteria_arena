import pygame
from settings import *
import utils
from game_arena import *
from board_generation import *


def draw_board_cells(screen, arena):
    screen.fill(BACKGROUND_COLOR)
    for c in BOARD_COORDINATES:
        cell = arena.board[c]
        if cell != EMPTY:  # cell contains bacteria
            if cell >= 0:  # bacteria
                cell_color = arena.bacteria_colors[cell]
            else:
                cell_color = WALL_COLOR
            rect = pygame.Rect(c[1] * SQUARE_SIZE, c[0] * SQUARE_SIZE + STATUS_BAR_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, cell_color, rect)


def draw_status_bar(screen, arena):
    b1_cnt, b2_cnt = arena.count_cells()
    b2_bar_size = round(b2_cnt / (b1_cnt + b2_cnt) * SCREEN_DIMENSIONS[0])
    b1_bar_size = SCREEN_DIMENSIONS[0] - b2_bar_size

    rect_2 = pygame.Rect(0, 0, b2_bar_size, STATUS_BAR_SIZE - STATUS_BAR_SEPARATOR_SIZE)
    rect_1 = pygame.Rect(b2_bar_size, 0, b1_bar_size, STATUS_BAR_SIZE - STATUS_BAR_SEPARATOR_SIZE)
    separator_rect = pygame.Rect(0, STATUS_BAR_SIZE - STATUS_BAR_SEPARATOR_SIZE, SCREEN_DIMENSIONS[0],
                                 STATUS_BAR_SEPARATOR_SIZE)
    pygame.draw.rect(screen, arena.bacteria_colors[0], rect_1)
    pygame.draw.rect(screen, arena.bacteria_colors[1], rect_2)
    # middle point marker
    pygame.draw.line(screen, BACKGROUND_COLOR, (SCREEN_DIMENSIONS[0] // 2, 0),
                     (SCREEN_DIMENSIONS[0] // 2, STATUS_BAR_SIZE - STATUS_BAR_SEPARATOR_SIZE), 1)
    pygame.draw.rect(screen, STATUS_BAR_SEPARATOR_COLOR, separator_rect)


def display_match(bacteria_1, bacteria_2, endless=False):
    arena = Arena(bacteria_1, bacteria_2, generate_board())

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
    pygame.display.set_caption(f'{bacteria_1.name} vs {bacteria_2.name}')

    screen.fill(BACKGROUND_COLOR)

    close = False
    stopped = False
    cnt = 1
    turns = 0
    while not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stopped = not stopped

        if not stopped and cnt % DISPLAY_SPEED_DELAY == 0:
            arena.run_iteration()
            turns += 1
            if turns == MATCH_LENGTH and not endless:
                winner = utils.largest_bacteria(arena.count_cells())
                print("\n---------- Match Ended ----------")
                print(f"winner: player number = {winner + 1}, bacteria name = {arena.bacterias[winner].name},"
                      f" bacteria id = {arena.bacterias[winner].get_bacteria_id()}")
                return winner

        cnt += 1
        draw_board_cells(screen, arena)
        draw_status_bar(screen, arena)

        pygame.display.update()
