import pygame
from cannon.const import BORDER, GRID, DARK, PIECE_RADIUS, OUTLINE, BLACK, TOWN, TOWN_SIZE

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = BORDER + self.col * GRID
        self.y = BORDER + self.row * GRID
    
    def draw(self, win):
        pygame.draw.circle(win, BLACK, (self.x, self.y), PIECE_RADIUS + OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), PIECE_RADIUS)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
    
    def __repr__(self):
        return f"Piece: {str(self.row)}, {str(self.col)}, {str(self.color)}"

class Town():
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = BORDER + self.col * GRID
        self.y = BORDER + self.row * GRID
    
    def draw(self, win):
        win.blit(TOWN, (self.x - TOWN_SIZE//2, self.y - TOWN_SIZE//2))