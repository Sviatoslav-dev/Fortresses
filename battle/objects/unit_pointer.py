import pygame

from battle.game import game
from battle.socket_client import ws
from battle.sprites.cell_sprites import object_in_cell


class UnitPointer(pygame.sprite.Sprite):
    def __init__(self, unit, pos):
        super(UnitPointer, self).__init__()
        self.unit = unit
        self.color = (100, 100, 255)
        self.pos = pos

        self.surf = pygame.Surface((40, 40))
        self.surf.set_alpha(50)
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()

    def draw(self):
        game.screen.blit(self.surf, self.rect)

    async def move_click(self, current_cell):
        from battle.objects.buildings import Road
        cells = game.field.cells
        move = game.move

        selected_unit = \
            cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].objects[-1]

        if len(current_cell.objects) == 1:
            game.remove_unit_pointers()
            selected_unit_num = len(
                cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].objects) - 1
            cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].objects.pop(-1)
            prev_pos = move.selected_unit_pos
            move.selected_unit_pos = (current_cell.j, current_cell.i)
            game.remove_unit_pointers()
            selected_unit.replace(current_cell)
            current_cell.objects.append(selected_unit)

            if selected_unit.steps > 0:
                selected_unit.create_unit_pointers(current_cell, selected_unit)
                if not object_in_cell(cells[self.pos[0]][self.pos[1]],
                                      Road):
                    selected_unit.steps -= 1
            await ws.send_command({
                "action": "replace",
                "data": {
                    "x1": prev_pos[0],
                    "y1": prev_pos[1],
                    "el": selected_unit_num,
                    "x2": current_cell.j,
                    "y2": current_cell.i,
                }
            })
        elif len(current_cell.objects) > 1:
            if hasattr(selected_unit, "attack"):
                selected_unit.attack(current_cell)
