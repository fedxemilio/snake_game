import pygame
import random
from constants import *

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
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, block_size, block_size))

class Bomb:
    def __init__(self):
        self.x = random.randint(0, WIDTH // block_size - 1) * block_size
        self.y = random.randint(0, HEIGHT // block_size - 1) * block_size

    def position(self):
        return (self.x, self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, 'RED', (self.x, self.y, block_size, block_size))
