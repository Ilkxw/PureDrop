import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 480, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PureDrop Cleaner")

# Clock
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE]

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Drop class
class Drop(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((50, 70), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, color, [0, 0, 50, 70])
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.face = font.render(":D", True, WHITE)
        self.speed = 5

    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= self.speed

    def move_right(self):
        if self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.face, (self.rect.x + 15, self.rect.y + 20))

# Dirty Water class
class DirtyWater(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = random.choice(COLORS)
        self.image = pygame.Surface((60, 60))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(random.randint(30, WIDTH - 30), -30))
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

# Main game function
def main():
    run = True
    score = 0
    active_color_index = 0
    drop = Drop(COLORS[active_color_index])
    waters = pygame.sprite.Group()
    DROP_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(DROP_EVENT, 1000)

    while run:
        screen.fill((200, 220, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Switch color
                    active_color_index = (active_color_index + 1) % len(COLORS)
                    drop = Drop(COLORS[active_color_index])
            elif event.type == DROP_EVENT:
                waters.add(DirtyWater())

        # Move drop based on key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            drop.move_left()
        if keys[pygame.K_RIGHT]:
            drop.move_right()

        # Check for collisions
        waters.update()
        for water in waters:
            if drop.rect.colliderect(water.rect):
                if water.color == drop.color:
                    waters.remove(water)
                    score += 1

        waters.draw(screen)
        drop.draw(screen)

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        instructions = font.render("← → to move | SPACE to switch drop", True, (0, 0, 0))
        screen.blit(instructions, (10, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
