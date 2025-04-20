# PureDrop Purify Game (Python Version using Pygame)
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PureDrop Purify Game")

# Colors
BLUE = (173, 216, 230)
YELLOW = (255, 253, 208)
DIRTY_GREEN = (105, 240, 174)
CLEAN_BLUE = (0, 191, 255)
WHITE = (255, 255, 255)
TEXT_COLOR = (0, 121, 107)

# Font
font = pygame.font.SysFont(None, 36)

# Game variables
score = 0
clock = pygame.time.Clock()
droplets = []
DROPLET_SIZE = 40
TIME_LIMIT = 60  # seconds
start_ticks = pygame.time.get_ticks()

# Droplet class
class Droplet:
    def __init__(self):
        self.x = random.randint(0, WIDTH - DROPLET_SIZE)
        self.y = random.randint(0, HEIGHT - DROPLET_SIZE)
        self.dirty = random.choice([True, False])
        self.color = DIRTY_GREEN if self.dirty else CLEAN_BLUE
        self.rect = pygame.Rect(self.x, self.y, DROPLET_SIZE, DROPLET_SIZE)

    def draw(self):
        pygame.draw.ellipse(screen, self.color, self.rect)

# Main loop
running = True
spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_event, 800)

while running:
    screen.fill(YELLOW)
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(0, TIME_LIMIT - seconds)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == spawn_event and time_left > 0:
            droplets.append(Droplet())

        if event.type == pygame.MOUSEBUTTONDOWN and time_left > 0:
            for droplet in droplets[:]:
                if droplet.rect.collidepoint(event.pos):
                    if droplet.dirty:
                        score += 1
                    droplets.remove(droplet)

    for droplet in droplets:
        droplet.draw()

    # Draw score and timer
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    timer_text = font.render(f"Time Left: {time_left}s", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (10, 50))

    if time_left == 0:
        result_text = font.render(f"Time's up! Final Score: {score}", True, TEXT_COLOR)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
