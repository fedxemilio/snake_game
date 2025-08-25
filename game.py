# add 1-hit shield, sturdy time for taking out bombs, map, levels, graphics
import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400 #make bigger

NORMAL_SPEED = 100
FAST_SPEED = 70

BONUS_PROB = 0.05
BOMB_PROB = 0.25

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
BLUE_NEGG = (0, 128, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)
CYAN = (0, 255, 255)
BROWN = (200, 165, 155)


NEGG_TYPES = [
    {"color": YELLOW, "points": 1, "weight": 80},
    {"color": GREEN, "points": 5, "weight": 12},
    {"color": BLUE_NEGG, "points": 10, "weight": 5},
    {"color": PURPLE, "points": 25, "weight": 2},
    {"color": GREY, "points": 100, "weight": 1},
]

BONUS_NEGGS = [
    {"color": ORANGE, "ability": "clear_bombs"},
    {"color": PINK, "ability": "cut_tail"},
    {"color": CYAN, "ability": "speed_up"},
    {"color": BROWN, "ability": "eat_bombs"}
]    

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meerca Chase Clone - Movement, Tail & Neggs")
clock = pygame.time.Clock()

#fonts
font = pygame.font.SysFont(None, 32)
game_over_font = pygame.font.SysFont(None, 64)
game_over_font2 = pygame.font.SysFont(None, 24)
death_text = "You Died"

block_size = 20

direction_map = {
    'UP': (0, -block_size),
    'DOWN': (0, block_size),
    'LEFT': (-block_size, 0),
    'RIGHT': (block_size, 0)
    }

left_turn = {
    'UP': 'LEFT',
    'DOWN': 'RIGHT',
    'LEFT': 'DOWN',
    'RIGHT': 'UP'
    }

right_turn = {
    'UP': 'RIGHT',
    'DOWN': 'LEFT',
    'LEFT': 'UP',
    'RIGHT': 'DOWN'
    }

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
        self.game_over = False

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

        if self.player.position() in self.player.tail[1:]:
            death_text = "(You just hit into your own tail!)"
            self.game_over = True

        elif self.player.position() in self.bombs:
            if not self.player.BOMB_EATER:
                death_text = "(You just ran straight into a bomb!)"
                self.game_over = True
            else:
                bomb_index = self.bombs.index((self.player.x, self.player.y))
                del self.bombs[bomb_index]
        
        elif self.player.position() == self.negg.position():
                    self.player.tail_length += 1
                    self.score += self.negg.points
                    self.negg = Negg()

                    if random.random() < BONUS_PROB:
                        self.bonus_negg = Negg(True)

                    if random.random() < BOMB_PROB:
                        self.bombs.append(((random.randint(0, WIDTH // block_size - 1) * block_size),
        (random.randint(0, HEIGHT // block_size - 1) * block_size)))
        
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
            pygame.draw.rect(screen, RED, (bomb[0], bomb[1], block_size, block_size))
        self.player.draw()
        self.negg.draw()
        if self.bonus_negg:
            self.bonus_negg.draw()
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
        

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.direction = 'UP'
        self.color = BLUE
        self.tail = []
        self.tail_length = 1
        self.BOMB_EATER = False

    def update(self):
        dx, dy = direction_map[self.direction]
        self.x += dx
        self.y += dy
        self.x %= WIDTH
        self.y %= HEIGHT

    def position(self):
        return (self.x, self.y)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, block_size, block_size)) #meerca
        for segment in self.tail:
            pygame.draw.rect(screen, self.color, (segment[0], segment[1], block_size, block_size)) # tail

class Negg:
    def __init__(self, bonus=False):
        self.bonus = bonus
        weights = [t["weight"] for t in NEGG_TYPES]
        chosen = random.choices(NEGG_TYPES, weights=weights)[0] if not self.bonus else random.choices(BONUS_NEGGS)[0]
        self.x = random.randint(0, WIDTH // block_size - 1) * block_size
        self.y = random.randint(0, HEIGHT // block_size - 1) * block_size
        self.color = chosen.get('color')
        self.points = chosen.get('points')
        self.ability = chosen.get('ability')
        
    def position(self):
        return (self.x, self.y)
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, block_size, block_size))


#GAME LOOP
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
        
                     

    











