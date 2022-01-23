
import pygame
from tkinter import Tk, messagebox
from cannon.game import Game
from cannon.params import WIDTH, HEIGHT, BORDER, GRID, AI_COLOR
from cannon.ai.algorithm import Ai

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
    ai = Ai(AI_COLOR)

    while run:
        clock.tick(FPS)

        if game.chickendinner():
            Tk().wm_withdraw()
            messagebox.showinfo(game.chickendinner(),"YOU'RE WINNER!")
            run = False
        
        if game.turn == AI_COLOR:
            if len(game.board.towns) < 2:
                game.random_town()
            else:
                best_score, move_board = ai.call_algorithm(game.board, 2)
                print(best_score)
                game.ai_move(move_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = select_pos(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

main()
