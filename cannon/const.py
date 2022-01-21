import pygame

WIDTH, HEIGHT = 600, 600
BORDER = 20
ROWS, COLS = 10, 10

GRID = (WIDTH-BORDER*2) // (COLS-1)

# Pieces
LIGHT = (255, 0, 0)
DARK = (105, 105, 105)

PADDING = 20
PIECE_RADIUS = GRID // 2 - PADDING
OUTLINE = 2

# Board & actions
LIGHT_BROWN = (232, 192, 134)
BROWN = (216, 130, 52)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

TOWN_SIZE = 80

TOWN = pygame.transform.scale(pygame.image.load("cannon/assets/town.png"), (TOWN_SIZE, TOWN_SIZE))