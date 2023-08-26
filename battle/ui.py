import pygame

from battle.constants import SCREEN_WIDTH
from battle.sprites.buttons import NextMoveButton


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.action_buttons = []
        self.next_move_button = NextMoveButton(720, 550, 10)
        self.next_move_button.active = True
        self.gold = None
        self.move_timer = None
        self.image = pygame.transform.scale(pygame.image.load("battle/icons/gold_coin.png"), (20, 20))

    def draw(self, gold, move_time, color):
        self.next_move_button.draw(self.screen)

        for button in self.action_buttons:
            if button.active:
                button.draw(self.screen)

        rendered_gold = self.gold.render(str(gold), 1, (255, 255, 255))
        self.screen.blit(rendered_gold, (SCREEN_WIDTH // 2, 0))
        rendered_move_time = self.gold.render(str(int(60 - move_time)), 1, color)
        self.screen.blit(rendered_move_time, (10, 0))
        self.screen.blit(self.image, (SCREEN_WIDTH // 2 - 20, 1))

    def remove_action_buttons(self):
        for button in self.action_buttons:
            button.active = False
        self.action_buttons = []

    def do_action_button_active(self, button):
        button.active = True
        self.action_buttons.append(button)

    def remove_action_button(self, button):
        button.active = False
        self.action_buttons.remove(button)
