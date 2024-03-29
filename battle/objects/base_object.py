from battle.game import game


class BaseObject:
    action_buttons = []

    def __init__(self, player):
        self.player = player
        self.color = (0, 0, 0)
        self.health_color = (255, 0, 0) if player is game.player2 else (0, 0, 255)

    def do_buttons_active(self):
        for button in self.action_buttons:
            if button not in game.ui.action_buttons:
                game.ui.do_action_button_active(button)
