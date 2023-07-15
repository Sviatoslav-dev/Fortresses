import pygame

from battle.custom_events import GRASS_CLICK
from battle.objects.buildings import Road
from battle.socket_client import ws
from battle.sprites.cell_sprites import remove_unit_pointers, object_in_cell


class UnitPointer:
    def __init__(self, unit, pos):
        self.unit = unit
        self.color = (100, 255, 100)
        self.pos = pos

    async def move_click(self, current_cell, move, cells, action_buttons):
        pygame.event.post(pygame.event.Event(GRASS_CLICK))
        can_go = True

        selected_unit = \
            cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].objects[-1]

        if can_go:
            remove_unit_pointers(move, cells)
            selected_unit_num = len(
                cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].objects) - 1
            cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].objects.pop(-1)
            prev_pos = move.selected_unit_pos
            move.selected_unit_pos = (current_cell.j, current_cell.i)
            remove_unit_pointers(move, cells)
            current_cell.objects.append(selected_unit)

            if selected_unit.steps > 0:
                selected_unit.create_unit_pointers(current_cell, selected_unit, move, cells)
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
