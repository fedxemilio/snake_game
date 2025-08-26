import pygame
import sys
from colors import *
from game import Game, screen, font, game_over_font, game_over_font2, death_text
from constants import *

game = Game()
while True:
    if not game.game_over:
        game.play()

    else:
        screen.fill(WHITE) #game over screen

        game_over_text = game_over_font.render("Game Over, you faggot", True, RED)
        game_over_text2 = game_over_font2.render(death_text, True, ORANGE)
        score_text = font.render(f"Final Score: {game.score}", True, BLACK)
        prompt_text = font.render("Press R to reset or Q to quit", True, BLACK)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 100))
        screen.blit(game_over_text2, (WIDTH // 2 - game_over_text2.get_width() // 2, 150))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 180))
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, 240))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
