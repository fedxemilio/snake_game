import pygame
from constants import WIDTH, HEIGHT, block_size, BLACK

LEVELS = [

    ["------------------------------",
     "------------------------------",
     "------------------------------",
     "----------1------1------------",
     "----------1------1------------",
     "----------1------1------------",
     "----------1------1------------",
     "------11111------11111--------",
     "------------------------------",
     "------------------------------",
     "------------------------------",
     "------------------------------",
     "------11111------11111--------",
     "----------1------1------------",
     "----------1------1------------",
     "----------1------1------------",
     "----------1------1------------",
     "------------------------------",
     "------------------------------",
     "------------------------------"
     ]
]

class Level:
    def __init__(self):
        self.level_index = 0
        self.map = LEVELS[self.level_index]

    def draw_level(self, screen):
        for y in range(HEIGHT // block_size):
            for x in range(WIDTH // block_size):
                if self.map[y][x] in "123":
                    pygame.draw.rect(screen, BLACK, (x*block_size, y*block_size, block_size, block_size))

    # accepts pixel coordinates
    def is_wall(self, coords):
        return self.map[coords[1] // block_size][coords[0] // block_size] in "123"

                    
