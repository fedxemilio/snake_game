from constants import WIDTH, HEIGHT, direction_map, block_size
from colors import BLUE
import pygame

head_up = pygame.transform.scale(pygame.image.load("assets/snake-head2.png"), (block_size, block_size))
body_vert = pygame.transform.scale(pygame.image.load("assets/snake_body_final.PNG"), (block_size, block_size))
body_hori = pygame.transform.rotate(body_vert, 90)
body_turn = pygame.transform.scale(pygame.image.load("assets/snake-turn2.png"), (block_size, block_size))
tail_up = pygame.transform.scale(pygame.image.load("assets/snake-tail-final.PNG"), (block_size, block_size))

head_images = {
    "UP": head_up,
    "DOWN": pygame.transform.rotate(head_up, 180),
    "LEFT": pygame.transform.rotate(head_up, 90),
    "RIGHT": pygame.transform.rotate(head_up, 270)
}

tail_images = {
    "UP": tail_up,
    "DOWN": pygame.transform.rotate(tail_up, 180),
    "LEFT": pygame.transform.rotate(tail_up, 90),
    "RIGHT": pygame.transform.rotate(tail_up, 270)
}

body_images = {
    "UO": body_turn,
    "OU": pygame.transform.rotate(body_turn, 180),
    "DO": pygame.transform.rotate(body_turn, 90),
    "OD": pygame.transform.rotate(body_turn, 270)

}

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.direction = 'UP'
        self.color = BLUE
        self.tail = []
        self.tail_length = 3
        self.BOMB_EATER = False

    def update(self):
        dx, dy = direction_map[self.direction]
        self.x += dx
        self.y += dy
        self.x %= WIDTH
        self.y %= HEIGHT

    def position(self):
        return (self.x, self.y)

    def draw(self, screen):
        for i, seg in enumerate(self.tail):
            if i == 0:
                screen.blit(head_images[self.direction], (self.x, self.y))
            elif i == len(self.tail) - 1:
                prev = self.tail[i - 1]
                if prev[0] < seg[0]:
                    direction = "LEFT"
                elif prev[0] > seg[0]:
                    direction = "RIGHT"
                elif prev[1] < seg[1]:
                    direction = "UP"
                else:
                    direction = "DOWN"
                screen.blit(tail_images[direction], (seg[0], seg[1]))
            else:
                prev = self.tail[i - 1]
                next = self.tail[i + 1]
                if prev[0] == next[0]:
                    screen.blit(body_vert, (seg[0], seg[1]))
                elif prev[1] == next[1]:
                    screen.blit(body_hori, (seg[0], seg[1]))

                elif prev[0] < seg[0] and next[1] < seg[1] or prev[1] < seg[1] and next[0] < seg[0]:
                        direction = "OU"
                        screen.blit(body_images[direction], (seg[0], seg[1]))
                elif prev[0] < seg[0] and next[1] > seg[1] or prev[1] > seg[1] and next[0] < seg[0]:
                        direction = "OD"
                        screen.blit(body_images[direction], (seg[0], seg[1]))
                elif prev[0] > seg[0] and next[1] < seg[1] or prev[1] < seg[1] and next[0] > seg[0]:
                        direction = "DO"
                        screen.blit(body_images[direction], (seg[0], seg[1]))
                elif prev[0] > seg[0] and next[1] > seg[1] or prev[1] > seg[1] and next[0] > seg[0]:
                        direction = "UO"
                        screen.blit(body_images[direction], (seg[0], seg[1]))
                    

                
                
        
    
        
