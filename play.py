import pygame
from constants import *
from game import Game

pygame.font.init()
pygame.display.set_caption("Connect 4")
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

agent = {
    "human": 0,
    "AI": 1
}

def play():
    game = Game(agent["human"], agent["AI"], 6)
    clock = pygame.time.Clock()
    run = True
    ai_processing = False

    while run:
        if not ai_processing:
            clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                game.make_move_human()
                WIN.fill((0, 0, 0))
                game.board.draw_board(WIN)
                pygame.display.update()
                ai_processing = True  

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.restart()

        if ai_processing:
            
            game.make_move_AI()
            ai_processing = False  

        WIN.fill((0, 0, 0))
        game.board.draw_board(WIN)
        pygame.display.update()

    pygame.quit()

play()
