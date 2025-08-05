#before negg types available
import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

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
    global x, y, direction, tail, tail_length, negg_x, negg_y, bombs, game_over
    x, y = WIDTH // 2, HEIGHT // 2
    direction = 'UP'
    tail = []
    tail_length = 1
    negg_x, negg_y = spawn_negg()
    bombs = []
    game_over = False

def spawn_negg():
    grid_width = WIDTH // block_size
    grid_height = HEIGHT // block_size
    return (
        random.randint(0, grid_width - 1) * block_size,
        random.randint(0, grid_height - 1) * block_size
    )

negg_x, negg_y = spawn_negg()
bombs = []

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

        for bomb in bombs:
            if x == bomb[0] and y == bomb[1]:
                print("Game Over faggot! You just ran straight into a bomb!")
                game_over = True

        if x == negg_x and y == negg_y:
            tail_length += 1
            negg_x, negg_y = spawn_negg()

            if random.random() < 0.25:
                bomb_x, bomb_y = spawn_negg()
                bombs.append((bomb_x, bomb_y))

        #draw
        screen.fill(WHITE)
        pygame.draw.rect(screen, YELLOW, (negg_x, negg_y, block_size, block_size)) #negg
        for bomb in bombs:
            pygame.draw.rect(screen, RED, (bomb[0], bomb[1], block_size, block_size)) #bomb
        pygame.draw.rect(screen, BLUE, (x, y, block_size, block_size)) #meerca
        for segment in tail:
            pygame.draw.rect(screen, BLUE, (segment[0], segment[1], block_size, block_size)) # tail
        score_text = font.render(f"Score: {tail_length - 1}", True, BLACK) # score
        screen.blit(score_text, (10, 10))
                             
        pygame.display.flip() #refresh
        #control speed
        clock.tick(10)
    else:
        screen.fill(WHITE) #game over screen

        game_over_text = game_over_font.render("Game Over, you faggot", True, RED)
        score_text = font.render(f"Final Score: {tail_length - 1}", True, BLACK)
        prompt_text = font.render("Press R to reset or Q to quit", True, BLACK)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 100))
        screen.blit(score_text, (WIDTH // 2 - score_tex.get_width() // 2, 180))
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, 240))

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
        
                     

    











