from constants import WIDTH, HEIGHT, direction_map, block_size
from colors import BLUE
import pygame

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

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, block_size, block_size)) #meerca
        for segment in self.tail:
            pygame.draw.rect(screen, self.color, (segment[0], segment[1], block_size, block_size)) # tail
