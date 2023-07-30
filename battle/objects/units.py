import pygame
import requests

from battle.cell_types import CellTypes
from battle.game import game
from battle.objects.base_object import BaseObject
from battle.objects.buildings import Mine, Fortress
from battle.objects.unit_pointer import UnitPointer
from battle.player import Player
from battle.sprites.action_buttons import BuildMine, BuildRoad


class Unit(BaseObject):
    def __init__(self, player):
        super().__init__(player)

    def create_unit_pointers(self, cell, clicked_object):
        from battle.objects.buildings import Road
        cells = game.field.cells
        move = game.move
        for cell_pos in [
            (cell.j + 1, cell.i), (cell.j + 1, cell.i + 1),
            (cell.j, cell.i + 1), (cell.j - 1, cell.i + 1),
            (cell.j - 1, cell.i), (cell.j - 1, cell.i - 1),
            (cell.j, cell.i - 1), (cell.j + 1, cell.i - 1),
        ]:
            print("CELL: ", cell_pos)
            try:
                curr_cell = cells[cell_pos[0]][cell_pos[1]]
                if cell_pos[0] >= 0 and cell_pos[1] >= 0:
                    curr_cell.is_open = True
                if ((
                    ((curr_cell.type == CellTypes.grass or curr_cell.type == CellTypes.gold)
                        and len(curr_cell.objects) == 0)
                    or isinstance(curr_cell.objects[-1], Road)
                    or ((isinstance(curr_cell.objects[-1], SwordsMan)
                         or isinstance(curr_cell.objects[-1], Builder)
                         or isinstance(curr_cell.objects[-1], Mine)
                         or isinstance(curr_cell.objects[-1], Fortress))
                        and curr_cell.objects[-1].player is not move.player
                        and isinstance(clicked_object, SwordsMan))
                ) and cell_pos[0] >= 0 and cell_pos[1] >= 0):
                    unit_pointer = UnitPointer(clicked_object, (cell_pos[0], cell_pos[1]))
                    cells[cell_pos[0]][cell_pos[1]].objects.append(unit_pointer)
                    move.unit_pointers.append(unit_pointer)
            except IndexError:
                pass


class SwordsMan(Unit, pygame.sprite.Sprite):
    def __init__(self, player: Player):
        super().__init__(player)
        super(SwordsMan, self).__init__(player)
        print(player.units_data)
        self.health = player.units_data["swordsman"]["heath"]#100
        self.damage = player.units_data["swordsman"]["heath"]#50
        self.color = (100, 255, 200)
        self.player = player
        self.player.units.append(self)
        self.steps = player.units_data["swordsman"]["steps"]#5

        self.player.move_price -= player.units_data["swordsman"]["step_price"]#5

        self.surf = pygame.Surface((30, 30))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()

        self.health_text = pygame.font.Font(None, 20)
        self.image = pygame.transform.scale(pygame.image.load("icons/swordsman.png"), (25, 30))

    def draw(self):
        game.screen.blit(self.image, self.rect)
        # pygame.draw.circle(game.screen, self.color, self.rect.center, self.rect.width / 2)
        rendered_health = self.health_text.render(str(self.health), 1, (255, 0, 0))
        game.screen.blit(rendered_health, (self.rect.center[0] - rendered_health.get_size()[0] // 2,
                                           self.rect.center[1] - 30))

    async def move_click(self, current_cell):
        game.remove_unit_pointers()

        game.move.selected_unit_pos = (current_cell.j, current_cell.i)
        game.remove_unit_pointers()
        if self.steps > 0:
            self.create_unit_pointers(current_cell, self)

    def replace(self, current_cell):
        pass

    def attack(self, current_cell, user_id):
        enemy = current_cell.objects[-2]
        enemy.health -= self.damage
        print("DAMAGE: ", current_cell.objects[-2].health)
        if enemy.health <= 0:
            if current_cell.objects[-2] in enemy.player.units:
                enemy.player.units.remove(current_cell.objects[-2])
            del current_cell.objects[-2]
            self.steps -= 1
            requests.get(f'http://127.0.0.1:8000/update_unit_stars?user_id={user_id}')

    def __del__(self):
        self.player.move_price += 5


class Builder(Unit, pygame.sprite.Sprite):
    action_buttons = [BuildMine(370, 550, 25), BuildRoad(430, 550, 25)]

    def __init__(self, player: Player):
        super().__init__(player)
        super(Builder, self).__init__(player)
        self.health = player.units_data["builder"]["heath"]#100
        self.color = (255, 100, 200)
        self.player = player
        self.player.units.append(self)
        self.steps = player.units_data["builder"]["steps"]#5

        self.player.move_price -= player.units_data["builder"]["step_price"]#5

        self.surf = pygame.Surface((15, 15))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()

        self.health_text = pygame.font.Font(None, 20)

    def draw(self):
        pygame.draw.circle(game.screen, self.color, self.rect.center, self.rect.width / 2)
        rendered_health = self.health_text.render(str(self.health), 1, (255, 0, 0))
        game.screen.blit(rendered_health, (self.rect.center[0] - rendered_health.get_size()[0] // 2,
                                           self.rect.center[1] - 30))

    async def move_click(self, current_cell):
        cells = game.field.cells
        move = game.move
        game.remove_unit_pointers()

        move.selected_unit_pos = (current_cell.j, current_cell.i)
        if self.steps > 0:
            game.remove_unit_pointers()
            self.create_unit_pointers(current_cell, self)

        if cells[move.selected_unit_pos[0]][
            move.selected_unit_pos[1]].type == CellTypes.gold:
            if self.action_buttons[0] not in game.ui.action_buttons:
                game.ui.do_action_button_active(self.action_buttons[0])
        elif self.action_buttons[0] in game.ui.action_buttons:
            game.ui.remove_action_button(self.action_buttons[0])

        if cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].type == CellTypes.grass:
            if self.action_buttons[1] not in game.ui.action_buttons:
                game.ui.do_action_button_active(self.action_buttons[1])
            print("CREATE BUTTON")
        elif self.action_buttons[1] in game.ui.action_buttons:
            game.ui.remove_action_button(self.action_buttons[1])

    def replace(self, current_cell):
        cells = game.field.cells
        move = game.move
        if (cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].type
                == CellTypes.gold):
            if self.action_buttons[0] not in game.ui.action_buttons:
                game.ui.do_action_button_active(self.action_buttons[0])
        elif self.action_buttons[0] in game.ui.action_buttons:
            game.ui.remove_action_button(self.action_buttons[0])

        if cells[move.selected_unit_pos[0]][
            move.selected_unit_pos[1]].type == CellTypes.grass:
            if self.action_buttons[1] not in game.ui.action_buttons:
                game.ui.do_action_button_active(self.action_buttons[1])
        elif self.action_buttons[1] in game.ui.action_buttons:
            game.ui.remove_action_button(self.action_buttons[1])

    def __del__(self):
        self.player.move_price += 5
