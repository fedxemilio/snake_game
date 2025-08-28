import pygame
import sys
import random
from constants import *
from player import Player
from objects import Negg, Bomb

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

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
        self.state = 'menu'

    def draw_text(self, text, x, y, color, size=36, centered=True):
        font = pygame.font.SysFont(None, size)
        rendered = font.render(text, True, color)
        rect = rendered.get_rect()
        if centered:
            rect.centerx = x
        else:
            rect.x = x
        rect.y = y
        screen.blit(rendered, rect)
        return rect

    def main_menu(self):
        events = pygame.event.get()
        screen.fill((30, 30, 30))
        self.draw_text("The Snake Game", WIDTH // 2, HEIGHT * 1/4, WHITE, size=48)

        start_btn = self.draw_text("Start Game", WIDTH // 2, HEIGHT // 2, WHITE)
        help_btn = self.draw_text("How to Play", WIDTH // 2, HEIGHT * 3/5, WHITE)
        settings_btn = self.draw_text("Settings", WIDTH // 2, HEIGHT * 2/3, WHITE)
        quit_btn = self.draw_text("Quit", WIDTH // 2, HEIGHT * 3/4, WHITE)

        mouse = pygame.mouse.get_pos()
        clicked = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)

        pygame.display.flip()

        if start_btn.collidepoint(mouse) and clicked:
            self.state = 'playing'
            return 'playing'
        elif help_btn.collidepoint(mouse) and clicked:
            self.state = 'help'
            return 'help'
        elif settings_btn.collidepoint(mouse) and clicked:
            self.state = 'settings'
            return 'settings'
        elif quit_btn.collidepoint(mouse) and clicked:
            pygame.quit()
            sys.exit()

    def help_menu(self):
        screen.fill(WHITE)
        self.draw_text("How To Play", WIDTH // 2, HEIGHT//20, BLACK, size=64)
        text = ["The snake must go around collecting neggs all while avoiding hitting its",
        "own tail (or the bombs). Press the LEFT button to make a left turn and",
        "RIGHT button to make a right turn. Neggs will increase your snake's tail",
        "and earn points according to their color. Powerups will also appear to help!",
        "Press the H key while playing to view this menu."]
        padding = HEIGHT // 20
        for i in range(len(text)):
            self.draw_text(text[i], WIDTH//50, (HEIGHT * 1/5 + padding*i), BLACK, size=24, centered=False)
        self.draw_text("Negg Types", WIDTH//10, HEIGHT//2, BLACK, centered=False)
        y_padding = 10
        for i in range(len(NEGG_TYPES)):
            y = (HEIGHT * 3/5) + (block_size + y_padding) * i
            pygame.draw.rect(screen, NEGG_TYPES[i].get('color'), (WIDTH//10, y, block_size, block_size))
            self.draw_text(f"{NEGG_TYPES[i].get('points')}pts", WIDTH//10 + block_size + y_padding, y, BLACK, size=16, centered=False)
        self.draw_text("Powerup Types", WIDTH * 3/5, HEIGHT//2, BLACK, centered=False)
        for i in range(len(BONUS_NEGGS)):
            y = (HEIGHT * 3/5) + (block_size + y_padding) * i
            pygame.draw.rect(screen, BONUS_NEGGS[i].get('color'), (WIDTH * 3/5, y, block_size, block_size))
            self.draw_text(BONUS_NEGGS[i].get('description'), WIDTH*3/5 + block_size + y_padding, y, BLACK, size=16, centered=False)

        back_btn = self.draw_text("Back", WIDTH*9/10, HEIGHT//20, BLACK)
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        clicked = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)

        if back_btn.collidepoint(mouse) and clicked:
            self.state = 'menu'
            return 'menu'

        pygame.display.flip()

    def get_help_menu(self):
        while True:
            pan_width, pan_height = WIDTH*4/5, HEIGHT*4/5
            panel = pygame.Surface((pan_width, pan_height))
            panel.fill(BLACK)
            screen.blit(panel, (WIDTH//2 - pan_width//2, HEIGHT//2 - pan_height//2))

            self.draw_text("Negg Types", WIDTH//8, HEIGHT*1/5, WHITE, centered=False)
            y_padding = 10
            for i in range(len(NEGG_TYPES)):
                y = (HEIGHT * 2/5) + (block_size + y_padding) * i
                pygame.draw.rect(screen, NEGG_TYPES[i].get('color'), (WIDTH//8, y, block_size, block_size))
                self.draw_text(f"{NEGG_TYPES[i].get('points')}pts", WIDTH//8 + block_size + y_padding, y, WHITE, size=16, centered=False)
            self.draw_text("Powerup Types", WIDTH * 2/5, HEIGHT*1/5, WHITE, centered=False)
            for i in range(len(BONUS_NEGGS)):
                y = (HEIGHT * 2/5) + (block_size + y_padding) * i
                pygame.draw.rect(screen, BONUS_NEGGS[i].get('color'), (WIDTH * 2/5, y, block_size, block_size))
                self.draw_text(BONUS_NEGGS[i].get('description'), WIDTH*2/5 + block_size + y_padding, y, WHITE, size=16, centered=False)

            pygame.display.flip()
            
            back_btn = self.draw_text("Back", WIDTH*9/10, HEIGHT//20, BLACK)
            events = pygame.event.get()
            mouse = pygame.mouse.get_pos()
            clicked = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)

            if back_btn.collidepoint(mouse) and clicked:
                break

    def settings(self):
        events = pygame.event.get()
        screen.fill(BLACK)
        self.draw_text("Settings", WIDTH // 2, HEIGHT * 1/4, WHITE, size=48)

        start_btn = self.draw_text("Start Game", WIDTH // 2, HEIGHT // 2, WHITE)
        settings_btn = self.draw_text("Settings", WIDTH // 2, HEIGHT * 2/3, WHITE)
        back_btn = self.draw_text("Back", WIDTH // 2, HEIGHT * 3/4, WHITE)

        mouse = pygame.mouse.get_pos()
        clicked = any(event.type == pygame.MOUSEBUTTONDOWN for event in events)

        pygame.display.flip()

        if start_btn.collidepoint(mouse) and clicked:
            self.state = 'playing'
            return 'playing'
        elif settings_btn.collidepoint(mouse) and clicked:
            self.state = 'settings'
            return 'settings'
        elif back_btn.collidepoint(mouse) and clicked:
            self.state = 'menu'
            return 'menu'

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
                elif event.key == pygame.K_h:
                    self.get_help_menu()

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

        self.draw_text(f"Score: {self.score}", 10, 10, BLACK, size=24, centered=False)
                             
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

        self.draw_text("Game Over!", WIDTH // 2, 100, size=64, color=BLUE, centered=True)
        self.draw_text("You Died.", WIDTH // 2, 150, size=26, color=ORANGE, centered=True)
        self.draw_text(f"Final Score: {self.score}", WIDTH // 2, 180, BLACK)
        self.draw_text("Press R to reset or Q to quit", WIDTH // 2, 240, BLACK)
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


