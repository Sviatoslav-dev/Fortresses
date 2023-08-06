import pygame
import random
from pygame.constants import K_UP, K_DOWN, K_LEFT, K_RIGHT

from battle.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((0, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)
        self.image = pygame.transform.scale(pygame.image.load("battle/icons/fortress.png"), (20, 20))

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    screen.fill((255, 255, 255))

    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # surf = pygame.Surface((50, 50))
    # surf.fill((0, 0, 0))
    # pygame.draw.circle(surf, (0, 0, 255), (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 20)
    # screen.blit(surf, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    # screen.blit(player.surf, player.rect)

    for entity in all_sprites:
        if hasattr(entity, "image"):
            screen.blit(entity.image, entity.rect)
        else:
            screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
