import pygame
import sys
import random
from constants import *
from player import Player
from objects import Negg, Bomb

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meerca Chase Clone - Movement, Tail & Neggs")
clock = pygame.time.Clock()

#fonts
font = pygame.font.SysFont(None, 32)
game_over_font = pygame.font.SysFont(None, 64)
game_over_font2 = pygame.font.SysFont(None, 24)
death_text = "You Died"

class Game:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.player = Player()
        self.negg = Negg()
        self.bonus_negg = None
        self.bombs = []
        self.powerups = []
        self.score = 0
        self.speed_boost_timer = 0
        self.bomb_eater_timer = 0
        self.state = 'playing'

    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.direction = left_turn[self.player.direction] #change direction
                elif event.key == pygame.K_RIGHT:
                    self.player.direction = right_turn[self.player.direction]

        self.player.update()
        #update tail
        if self.player.tail_length > 0:
            self.player.tail.insert(0, self.player.position())
            if len(self.player.tail) > self.player.tail_length:
                self.player.tail.pop()

        for bomb in self.bombs:
            if self.player.position() == bomb.position():
                if not self.player.BOMB_EATER:
                    self.state = 'game over'
                    return 'game over'
                else:
                    bomb_index = self.bombs.index(bomb)
                    del self.bombs[bomb_index]

        if self.player.position() in self.player.tail[1:]:
            self.state = 'game over'
            return 'game over'

        
        elif self.player.position() == self.negg.position():
                    self.player.tail_length += 1
                    self.score += self.negg.points
                    self.negg = Negg()

                    if random.random() < BONUS_PROB:
                        self.bonus_negg = Negg(True)

                    if random.random() < BOMB_PROB:
                        self.bombs.append(Bomb())
        
        elif self.bonus_negg and self.player.position() == self.bonus_negg.position():
            if self.bonus_negg.ability == "clear_bombs":
                self.bombs.clear()
            elif self.bonus_negg.ability == "cut_tail": # logicccc
                for i in range(min(5, self.player.tail_length - 1)):
                    self.player.tail.pop()
                self.player.tail_length = max(1, self.player.tail_length - 5)
            elif self.bonus_negg.ability == "speed_up":
                self.speed_boost_timer = pygame.time.get_ticks() + 5000 #5 secs from now
            elif self.bonus_negg.ability == "eat_bombs":
                self.bomb_eater_timer = pygame.time.get_ticks() + 5000
            self.bonus_negg = None
 
        #draw
        screen.fill(WHITE)
        for bomb in self.bombs:
            bomb.draw(screen)
        self.player.draw(screen)
        self.negg.draw(screen)
        if self.bonus_negg:
            self.bonus_negg.draw(screen)
        score_text = font.render(f"Score: {self.score}", True, BLACK) # score
        screen.blit(score_text, (10, 10))
                             
        pygame.display.flip() #refresh
        #control speed
        if pygame.time.get_ticks() < self.speed_boost_timer:
            speed = FAST_SPEED
        else:
            speed = NORMAL_SPEED

        if pygame.time.get_ticks() < self.bomb_eater_timer:
            self.player.BOMB_EATER = True
            self.player.color = RED
        else:
            self.player.BOMB_EATER = False
            self.player.color = BLUE

            
        clock.tick(1000 // speed)

    def game_over(self):
        screen.fill(WHITE)

        game_over_text = game_over_font.render("Game Over, you faggot", True, RED)
        game_over_text2 = game_over_font2.render(death_text, True, ORANGE)
        score_text = font.render(f"Final Score: {self.score}", True, BLACK)
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
                    self.reset()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


