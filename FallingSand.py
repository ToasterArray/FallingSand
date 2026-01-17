import numpy as np
import pygame
from pygame.locals import KEYDOWN, K_q
import sys
import copy
import os
import random

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (460,30)
SANDCOLOR = (212, 179, 61)
STONECOLOR = (41, 47, 52)
SCREENSIZE = WIDTH, HEIGHT = 1000, 1000
CELL_S = 10
ROWS = WIDTH // CELL_S
COLS = HEIGHT // CELL_S
surf = pygame.display.set_mode(SCREENSIZE, 0, -5)
pygame.display.set_caption("Sand")
CELLS = np.zeros((ROWS, COLS))
clock = pygame.time.Clock()

# materials:
sand = 1
stone = 2

def main():
    global CELLS
    pygame.init()
    pygame.font.init()
    text_font = pygame.font.SysFont('Consolas', 30)
    pygame.mouse.set_visible(False)
    surf.fill('black')
    while True:
        
        surf.fill('black')
        clock.tick()
        text_surface = text_font.render(f'FPS: {round(clock.get_fps(), 1)}', False, 'white')
        checkEvents()
        CELLS = update_sand(surf, CELLS)
        surf.blit(text_surface, (0,0))
        if pygame.mouse.get_pressed()[0]:
            add_pixel(CELLS, pygame.mouse.get_pos(), surf, sand)
        elif pygame.mouse.get_pressed()[2]:
            remove_pixel(CELLS, pygame.mouse.get_pos(), surf)
        elif pygame.mouse.get_pressed()[1]:
            add_pixel(CELLS, pygame.mouse.get_pos(), surf, stone)
        draw_brush(surf, pygame.mouse.get_pos())
        pygame.display.update()

def update_sand(screen, cells):
    updated_cells = copy.deepcopy(cells)
    direction = random.choice(['left', 'right'])
    for row in range(cells.shape[0]):
        if sum(cells[row]) == 0:
            continue
        for col in range(cells.shape[1]):
            if cells[row][col] == sand:   
                if row + 1 < ROWS and cells[row + 1][col] == 0:
                    updated_cells[row][col] = 0
                    updated_cells[row + 1][col] = 1
                elif row + 1 < ROWS and col - 1 >= 0 and cells[row + 1][col - 1] == 0 and direction == 'left':
                    updated_cells[row][col] = 0
                    updated_cells[row + 1][col - 1] = 1
                elif row + 1 < ROWS and col + 1 < COLS and cells[row + 1][col + 1] == 0 and direction == 'right':
                    updated_cells[row][col] = 0
                    updated_cells[row + 1][col + 1] = 1
            if cells[row, col] == 0:
                color = 'black'
            elif cells[row, col] == sand:
                color = SANDCOLOR
            else:
                color = STONECOLOR
            # Draw the cell
            pygame.draw.rect(screen, color, (col * CELL_S, row * CELL_S, CELL_S, CELL_S))
    return updated_cells

def add_pixel(cells, position, screen, mat):
    x = round(position[0] / 10)
    y = round(position[1] / 10)
    if mat == sand and x < COLS and y < ROWS - 1 and cells[y, x] == 0 and (cells[y + 1][x] == 0 or cells[y + 1][x - 1]):
        cells[y, x] = 1
        pygame.draw.rect(screen, SANDCOLOR, (x * CELL_S, y * CELL_S, CELL_S, CELL_S))
    elif mat == stone and x < COLS and y < ROWS - 1 and cells[y, x] == 0:
        cells[y, x] = 2
        pygame.draw.rect(screen, 'white', (x * CELL_S, y * CELL_S, CELL_S, CELL_S))


def remove_pixel(cells, position, screen):
    x = round(position[0] / 10)
    y = round(position[1] / 10)
    if x < COLS and y < ROWS:
        cells[y, x] = 0
    pygame.draw.rect(screen, 'black', (x * CELL_S, y * CELL_S, CELL_S, CELL_S))

def rand_color(sand_color):
    r, g, b = sand_color
    color = (r + random.randint(-10, 10), g + random.randint(-10, 10), b + random.randint(-10, 10))
    return color

def draw_brush(screen, pos):
    x = round(pos[0] / 10)
    y = round(pos[1] / 10)
    pygame.draw.rect(screen, 'white', (x * CELL_S, y * CELL_S, CELL_S, CELL_S))

def checkEvents():  # event handler
    global RUNNING
    global GEN
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()
        '''elif pygame.mouse.get_pressed()[0]:
            try:
                add_sand(CELLS, pygame.mouse.get_pos(), surf)
            except AttributeError:
                pass'''

if __name__ == '__main__':
    main()