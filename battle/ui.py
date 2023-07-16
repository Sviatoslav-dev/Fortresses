from battle.sprites.buttons import NextMoveButton


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.action_buttons = []
        self.next_move_button = NextMoveButton(750, 580, 10)

        self.next_move_button.active = True

    def draw(self):
        self.next_move_button.draw(self.screen)

        for button in self.action_buttons:
            if button.active:
                button.draw(self.screen)

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
