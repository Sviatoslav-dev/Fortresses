import pygame

from battle.constants import SCREEN_WIDTH
from battle.sprites.buttons import NextMoveButton


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.action_buttons = []
        self.next_move_button = NextMoveButton(750, 580, 10)
        self.next_move_button.active = True
        self.gold = None

    def draw(self, gold):
        self.next_move_button.draw(self.screen)

        for button in self.action_buttons:
            if button.active:
                button.draw(self.screen)

        rendered_gold = self.gold.render(str(gold), 1, (0, 0, 255))
        self.screen.blit(rendered_gold, (SCREEN_WIDTH // 2 - 90, 0))

    def remove_action_buttons(self):
        print("REMOVE ACTION BUTTON")
        for button in self.action_buttons:
            button.active = False
        self.action_buttons = []

    def do_action_button_active(self, button):
        button.active = True
        self.action_buttons.append(button)

    def remove_action_button(self, button):
        button.active = False
        self.action_buttons.remove(button)
