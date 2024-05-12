#pygame==2.1.2
#pygame-sdl2==7.3.5


import pygame
import random

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Box Shooter")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load sound files
shooting_sound = pygame.mixer.Sound("C:\\python_test_data\\shooting_block_game\\game_music\\laser.mp3")
explosion_sound = pygame.mixer.Sound("C:\\python_test_data\\shooting_block_game\\game_music\\explosion.mp3")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 30
        self.height = 25
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

# Enemy class
class Huddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = random.randint(50, 100)
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.width)
        self.rect.y = random.randint(-50, -self.height)
        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - self.width)
            self.rect.y = random.randint(-50, -self.height)
            self.speed_y = random.randint(1, 3)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Group for all sprites
all_sprites = pygame.sprite.Group()
huddles = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create huddles
for _ in range(8):
    huddle = Huddle()
    all_sprites.add(huddle)
    huddles.add(huddle)

# Score
score = 0
font = pygame.font.Font(None, 36)

# Main loop
running = True
clock = pygame.time.Clock()
huddle_count = 0

while running:
    clock.tick(60)

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shooting_sound.play()  # Play shooting sound
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Update
    all_sprites.update()

    # Check collisions (player with huddles)
    if pygame.sprite.spritecollide(player, huddles, dokill=False):
        # Game over condition
        running = False

    # Check collisions (bullets with huddles)
    hits = pygame.sprite.groupcollide(huddles, bullets, True, True)
    for hit in hits:
        explosion_sound.play()  # Play explosion sound
        huddle_count += 1
        score += 1
        if huddle_count % 20 == 0:
            for huddle in huddles:
                huddle.speed_y += 1
        huddle = Huddle()
        all_sprites.add(huddle)
        huddles.add(huddle)

    # Draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    # Display Score
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

# Game over screen
game_over_font = pygame.font.Font(None, 72)
game_over_text = game_over_font.render("Game Over", True, WHITE)
game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
screen.blit(game_over_text, game_over_rect)

final_score_text = font.render("Final Score: " + str(score), True, WHITE)
final_score_rect = final_score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
screen.blit(final_score_text, final_score_rect)

pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.delay(3000)

# Quit
pygame.quit()
