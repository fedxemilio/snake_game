import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400

NORMAL_SPEED = 100
FAST_SPEED = 70

speed_boost_timer = 0

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


NEGG_TYPES = [
    {"color": YELLOW, "points": 1, "weight": 80},
    {"color": GREEN, "points": 5, "weight": 12},
    {"color": BLUE_NEGG, "points": 10, "weight": 5},
    {"color": PURPLE, "points": 25, "weight": 2},
    {"color": GREY, "points": 100, "weight": 1},
]

BONUS_NEGGS = [
    (ORANGE, "clear_bombs"),
    (PINK, "cut_tail"),
    (CYAN, "speed_up"),
]
    

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meerca Chase Clone - Movement, Tail & Neggs")

#fonts
font = pygame.font.SysFont(None, 32)
game_over_font = pygame.font.SysFont(None, 64)

#meerca set_up
block_size = 20
x, y = WIDTH // 2, HEIGHT // 2 #starting position
direction = 'UP'
#meerca tail
tail_size = 20
tail = []
tail_length = 1 #avoid glitch
score = 0

bombs = []
is_bonus_negg = False
bonus_negg = None

#movement
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

clock = pygame.time.Clock()
game_over = False

def reset_game():
    global x, y, direction, tail, tail_length, score, negg, bombs, game_over
    x, y = WIDTH // 2, HEIGHT // 2
    direction = 'UP'
    tail = []
    tail_length = 1
    score = 0
    negg = spawn_random_negg()
    bombs = []
    game_over = False

def spawn_random_negg():
    weights = [t["weight"] for t in NEGG_TYPES]
    chosen = random.choices(NEGG_TYPES, weights=weights)[0]

    while True: # prevent spawning on a bomb
        pos_x, pos_y = spawn_random_position()
        if (pos_x, pos_y) not in bombs:
            break
    return (pos_x, pos_y, chosen) # tuple rather than dict

def spawn_random_position():
    grid_width = WIDTH // block_size
    grid_height = HEIGHT // block_size
    if is_bonus_negg: # bonus negg spawn
        return (
            random.randint(0, grid_width - 1) * block_size,
            random.randint(0, grid_height - 1) * block_size,
            random.choices(BONUS_NEGGS)[0]
        )
    return (
        random.randint(0, grid_width - 1) * block_size,
        random.randint(0, grid_height - 1) * block_size
    )

negg = spawn_random_negg()


#GAME LOOP

while True:
    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = left_turn[direction] #change direction
                elif event.key == pygame.K_RIGHT:
                    direction = right_turn[direction]

        #move meerca
        dx, dy = direction_map[direction]
        x += dx
        y += dy
        #wrap around
        x %= WIDTH
        y %= HEIGHT

        #update tail
        if tail_length > 0:
            tail.insert(0, (x, y))
            if len(tail) > tail_length:
                tail.pop()

        if (x, y) in tail[1:]:
            print("Game Over faggot! You just hit into your own tail!")
            game_over = True

        if (x, y) in bombs:
            print("Game Over faggot! You just ran straight into a bomb!")
            game_over = True

        if (x, y) == negg[:2]:
            tail_length += 1
            score += negg[2]["points"]
            negg = spawn_random_negg()

            if random.random() < 0.05:
                is_bonus_negg = True
                bonus_negg = spawn_random_position()
                is_bonus_negg = False

            if random.random() < 0.25:
                bomb_x, bomb_y = spawn_random_position()
                if (bomb_x, bomb_y) != negg[:2]:
                    bombs.append((bomb_x, bomb_y))

        if bonus_negg and (x, y) == bonus_negg[:2]:
            if bonus_negg[2][1] == "clear_bombs":
                bombs.clear()
            elif bonus_negg[2][1] == "cut_tail": # logicccc
                for i in range(min(5, tail_length - 1)):
                               tail.pop()
                tail_length = max(1, tail_length - 5)
            elif bonus_negg[2][1] == "speed_up":
                speed_boost_timer = pygame.time.get_ticks() + 5000 #5 secs from now
            bonus_negg = None
            

        #draw
        screen.fill(WHITE)
        pygame.draw.rect(screen, negg[2]["color"], (negg[0], negg[1], block_size, block_size)) #negg
        if bonus_negg:
            pygame.draw.rect(screen, bonus_negg[2][0], (bonus_negg[0], bonus_negg[1], block_size, block_size)) #bonusnegg
        for bomb in bombs:
            pygame.draw.rect(screen, RED, (bomb[0], bomb[1], block_size, block_size)) #bomb
        pygame.draw.rect(screen, BLUE, (x, y, block_size, block_size)) #meerca
        for segment in tail:
            pygame.draw.rect(screen, BLUE, (segment[0], segment[1], block_size, block_size)) # tail
        score_text = font.render(f"Score: {score}", True, BLACK) # score
        screen.blit(score_text, (10, 10))
                             
        pygame.display.flip() #refresh
        #control speed
        if pygame.time.get_ticks() < speed_boost_timer:
            speed = FAST_SPEED
        else:
            speed = NORMAL_SPEED
            
        clock.tick(1000 // speed)
    else:
        screen.fill(WHITE) #game over screen

        game_over_text = game_over_font.render("Game Over, you faggot", True, RED)
        score_text = font.render(f"Final Score: {score}", True, BLACK)
        prompt_text = font.render("Press R to reset or Q to quit", True, BLACK)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 100))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 180))
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, 240))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        
                     

    











