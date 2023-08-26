import pygame

from battle.custom_events import NEXT_MOVE


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super(Button, self).__init__()
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.color = (200, 100, 100)
        self.radius = radius
        self.active = False


class NextMoveButton(Button):
    def __init__(self, x, y, radius):
        super(NextMoveButton, self).__init__(x, y, radius)
        self.rect = pygame.Rect(x - radius, y - radius, 50, 50)
        self.color = (255, 255, 255)
        self.image = pygame.transform.scale(pygame.image.load("battle/icons/next_move_white.png"), (50, 50))

    async def on_click(self, pos):
        if self.rect.collidepoint(pos) and self.active:
            pygame.event.post(pygame.event.Event(NEXT_MOVE))
            return True
        else:
            return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
