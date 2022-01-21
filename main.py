
import pygame

from cannon.game import Game
from cannon.const import WIDTH, HEIGHT, BORDER, GRID

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cannon")

def select_pos(pos):
    x, y = pos
    row = round((y - BORDER) / GRID)
    col = round((x - BORDER) / GRID)
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.winner():
            print(f"{game.winner()} wins!")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = select_pos(pos)
                # if game.turn == LIGHT:
                game.select(row, col)

        game.update()

        # select_town_place(row, col, color)
        # board.draw_town(WIN, row, col, color)

    pygame.quit()

main()
