import pygame

from cannon import parameters

FPS = 60

WIN = pygame.display.set_mode((parameters.WIDTH, parameters.HEIGHT))
pygame.display.set_caption("Cannon")

def main():
    run = True
    clock = pygame.time.Clock(FPS)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

    pygame.quit()