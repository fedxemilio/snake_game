import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
MEERCA_SIZE = 50
FRUIT_SIZE = 30

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meerca Chase Clone")

# Fonts
font = pygame.font.SysFont("Arial", 30)

# Player Class (Meerca)
class Meerca(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((MEERCA_SIZE, MEERCA_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep Meerca inside the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Fruit Class (Collectable items)
class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((FRUIT_SIZE, FRUIT_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - FRUIT_SIZE)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - FRUIT_SIZE)

# Set up sprite groups
all_sprites = pygame.sprite.Group()
fruits = pygame.sprite.Group()

# Create Meerca
meerca = Meerca()
all_sprites.add(meerca)

# Create fruits
for _ in range(5):  # Create 5 fruits
    fruit = Fruit()
    all_sprites.add(fruit)
    fruits.add(fruit)

# Score
score = 0

# Game Loop
clock = pygame.time.Clock()
running = True
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Collision detection: Meerca collects fruits
    collided_fruits = pygame.sprite.spritecollide(meerca, fruits, True)
    for fruit in collided_fruits:
        score += 1  # Increase score when collecting a fruit
        # Create a new fruit after collecting one
        new_fruit = Fruit()
        all_sprites.add(new_fruit)
        fruits.add(new_fruit)

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update the screen
    pygame.display.flip()

    # Maintain frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
