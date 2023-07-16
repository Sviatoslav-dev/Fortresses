from battle.cell_types import CellTypes
from battle.game import game
from battle.objects.base_object import BaseObject
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
            (cell.j + 1, cell.i),
            (cell.j + 1, cell.i + 1),
            (cell.j, cell.i + 1),
            (cell.j - 1, cell.i + 1),
            (cell.j - 1, cell.i),
            (cell.j - 1, cell.i - 1),
            (cell.j, cell.i - 1),
            (cell.j + 1, cell.i - 1),
        ]:
            try:
                cell = cells[cell_pos[0]][cell_pos[1]]
                if ((cell.type == CellTypes.grass or
                     cell.type == CellTypes.gold) and
                    len(cell.objects) == 0) or \
                        isinstance(cell.objects[-1], Road) or (
                        (isinstance(cell.objects[-1], SwordsMan) or isinstance(cell.objects[-1],
                                                                               Builder)) and
                        cell.objects[-1].player is not move.player and isinstance(clicked_object,
                                                                                  SwordsMan)
                ):
                    unit_pointer = UnitPointer(clicked_object, (cell_pos[0], cell_pos[1]))
                    cells[cell_pos[0]][cell_pos[1]].objects.append(unit_pointer)
                    move.unit_pointers.append(unit_pointer)
            except IndexError:
                pass


class SwordsMan(Unit):
    def __init__(self, player: Player):
        super().__init__(player)
        self.health = 100#player.units_data["swords_man"]["health"]#100
        self.damage = 50#player.units_data["swords_man"]["health"]#50
        self.color = (100, 255, 200)
        self.player = player
        self.player.units.append(self)
        self.steps = 5

        self.player.move_price -= 5

    async def move_click(self, current_cell):
        game.remove_unit_pointers()

        game.move.selected_unit_pos = (current_cell.j, current_cell.i)
        game.remove_unit_pointers()
        if self.steps > 0:
            self.create_unit_pointers(current_cell, self)

    def replace(self, current_cell):
        if len(current_cell.objects) > 1:
            if (isinstance(current_cell.objects[-2], SwordsMan) or
                    isinstance(current_cell.objects[-2], Builder)):
                current_cell.objects[-2].health -= self.damage
                print("DAMAGE: ", current_cell.objects[-2].health)
                if current_cell.objects[-2].health <= 0:
                    current_cell.objects[-2].player.units.remove(current_cell.objects[-2])
                    del current_cell.objects[-2]
                    self.steps -= 1
                # else:
                #     can_go = False

    def __del__(self):
        self.player.move_price += 5


class Builder(Unit):
    action_buttons = [BuildMine(370, 550, 25), BuildRoad(430, 550, 25)]

    def __init__(self, player: Player):
        super().__init__(player)
        print(player.units_data)
        self.health = 100#player.units_data["builder"]["health"]#100
        self.color = (255, 100, 200)
        self.player = player
        self.player.units.append(self)
        self.steps = 5

        self.player.move_price -= 5

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
