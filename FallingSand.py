import numpy as np
import pygame
from pygame.locals import KEYDOWN, K_q, K_1, K_2, K_3
import sys
import copy
import os
import random

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (460,30)  # sets window position
SANDCOLOR = (212, 179, 61)
STONECOLOR = (41, 47, 52)
WATERCOLOR = (0, 0, 210)
SCREENSIZE = WIDTH, HEIGHT = 1000, 1000
CELL_S = 10
ROWS = WIDTH // CELL_S
COLS = HEIGHT // CELL_S
surf = pygame.display.set_mode(SCREENSIZE, 0, -5)
pygame.display.set_caption("Sand")
CELLS = np.zeros((ROWS, COLS))  # creates a 2D list of zeros for storing particle data
clock = pygame.time.Clock()  # creates a clock for measuring fps

# materials:
sand = 3
stone = 2
water = 1
current_material = sand
# main game loop
def main(cells):
    pygame.init()
    pygame.font.init()
    text_font = pygame.font.SysFont('Consolas', 30)
    pygame.mouse.set_visible(False)
    surf.fill('black')
    while True:
        pygame.time.wait(10)
        surf.fill('black')  # prevents fps counter text from writing on top of itself
#region FPS counter       
        clock.tick()
        text_surface = text_font.render(f'FPS: {round(clock.get_fps(), 1)}', False, 'white')
        surf.blit(text_surface, (0,0))
#endregion
        checkEvents()
        cells = update_sand(surf, cells)
#region Temp Brush Handler        
        if pygame.mouse.get_pressed()[0]:
            add_pixel(cells, pygame.mouse.get_pos(), surf, current_material)
        elif pygame.mouse.get_pressed()[2]:
            remove_pixel(cells, pygame.mouse.get_pos(), surf)
        draw_brush(surf, pygame.mouse.get_pos())
#endregion        
        pygame.display.update()

# particle updater
def update_sand(screen, cells):
    updated_cells = copy.deepcopy(cells)  # buffer for updating cells
    direction = random.choice(['left', 'right'])  # random choice direction for sand piles
    for row in range(cells.shape[0]):
        if sum(cells[row]) == 0:  # optimisation - skips line if there are no particles present in it
            continue
        for col in range(cells.shape[1]):
            
            
            if cells[row][col] == water: # water physics
                w_direction = random.choice(['left', 'right'])
                if row + 1 < ROWS and updated_cells[row + 1][col] == 0 and cells[row + 1][col] == 0:  # fall straight down
                    updated_cells[row][col] = 0
                    updated_cells[row + 1][col] = water
                elif col - 1 >= 0 and updated_cells[row][col - 1] == 0 and cells[row][col - 1] == 0 and w_direction == 'left':  # move left
                    updated_cells[row][col] = 0
                    updated_cells[row][col - 1] = water
                elif col + 1 < COLS and updated_cells[row][col + 1] == 0 and cells[row][col + 1] == 0 and w_direction == 'right': # move right
                    updated_cells[row][col] = 0
                    updated_cells[row][col + 1] = water
                elif row + 1 < ROWS and col - 1 >= 0 and cells[row + 1][col - 1] == 0 and w_direction == 'left':  # fall left
                    updated_cells[row][col] = 0
                    updated_cells[row + 1][col - 1] = water
                elif row + 1 < ROWS and col + 1 < COLS and cells[row + 1][col + 1] == 0 and w_direction == 'right':  # fall right
                    updated_cells[row][col] = 0
                    updated_cells[row + 1][col + 1] = water
                else:
                    updated_cells[row][col] = water
            elif cells[row][col] == sand: # sand physics
                if row + 1 < ROWS and cells[row + 1][col] <= 1 and updated_cells[row + 1][col] <= 1:  # fall straight down
                    updated_cells[row][col] = updated_cells[row + 1][col]
                    updated_cells[row + 1][col] = sand
                elif row + 1 < ROWS and col - 1 >= 0 and cells[row + 1][col - 1] <= 1 and updated_cells[row + 1][col - 1] <= 1 and direction == 'left':  # fall left
                    updated_cells[row][col] = updated_cells[row + 1][col - 1]
                    updated_cells[row + 1][col - 1] = sand
                elif row + 1 < ROWS and col + 1 < COLS and cells[row + 1][col + 1] <= 1 and updated_cells[row + 1][col + 1] <= 1 and direction == 'right':  # fall right
                    updated_cells[row][col] = updated_cells[row + 1][col + 1]
                    updated_cells[row + 1][col + 1] = sand

            if cells[row, col] == 0:  # empty
                color = 'black'
            elif cells[row, col] == sand:  # sand
                color = SANDCOLOR
            elif cells[row, col] == stone:  # stone
                color = STONECOLOR
            elif cells[row, col] == water:
                color = WATERCOLOR
            # Draw the cell
            pygame.draw.rect(screen, color, (col * CELL_S, row * CELL_S, CELL_S, CELL_S))
    return updated_cells

# adds particle on mouse position
def add_pixel(cells, position, screen, mat):
    x = round(position[0] / 10)
    y = round(position[1] / 10)
    if mat == sand and x < COLS and y < ROWS - 1 and cells[y, x] == 0 and (cells[y + 1][x] == 0 or cells[y + 1][x - 1]):
        cells[y, x] = sand
        pygame.draw.rect(screen, SANDCOLOR, (x * CELL_S, y * CELL_S, CELL_S, CELL_S))
    elif mat == stone and x < COLS and y < ROWS - 1 and cells[y, x] == 0:
        cells[y, x] = stone
        pygame.draw.rect(screen, STONECOLOR, (x * CELL_S, y * CELL_S, CELL_S, CELL_S))
    elif mat == water and x < COLS and y < ROWS - 1 and cells[y, x] == 0:
        cells[y, x] = water
        pygame.draw.rect(screen, WATERCOLOR, (x * CELL_S, y * CELL_S, CELL_S, CELL_S))

# removes particle on mouse position
def remove_pixel(cells, position, screen):
    x = round(position[0] / 10)
    y = round(position[1] / 10)
    if x < COLS and y < ROWS:
        cells[y, x] = 0
    pygame.draw.rect(screen, 'black', (x * CELL_S, y * CELL_S, CELL_S, CELL_S))

# TODO: random particle color
def rand_color(sand_color):
    r, g, b = sand_color
    color = (r + random.randint(-10, 10), g + random.randint(-10, 10), b + random.randint(-10, 10))
    return color

# replaces cursor with square on grid
def draw_brush(screen, pos):
    x = round(pos[0] / 10)
    y = round(pos[1] / 10)
    pygame.draw.rect(screen, 'white', (x * CELL_S, y * CELL_S, CELL_S, CELL_S))

# event handler
def checkEvents():
    global RUNNING
    global GEN
    global current_material
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_1:
                current_material = sand
            elif event.key == K_2:
                current_material = stone
            elif event.key == K_3:
                current_material = water


if __name__ == '__main__':
    main(CELLS)