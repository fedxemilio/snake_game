import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CELL_SIZE = 20
FPS = 10
FONT = pygame.font.SysFont(None, 36)

# Colors
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BG_COLOR = (250, 250, 200)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meerca Chase (Clone)")
clock = pygame.time.Clock()

# Snake setup
snake = [(100, 100)]
direction = (CELL_SIZE, 0)
