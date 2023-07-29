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

        print(len(current_cell.objects))
        print((len(current_cell.objects) == 1 and Road not in current_cell.objects))
        print((len(current_cell.objects) == 2 and Road in current_cell.objects))
        if ((len(current_cell.objects) == 1 and not isinstance(current_cell.objects[0], Road)) or
        (len(current_cell.objects) == 2 and isinstance(current_cell.objects[0], Road))):
            game.remove_unit_pointers()
            selected_unit_num = len(
                cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].objects) - 1
            cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].objects.pop(-1)
            prev_pos = move.selected_unit_pos
            move.selected_unit_pos = (current_cell.j, current_cell.i)
            game.remove_unit_pointers()
            selected_unit.replace(current_cell)
            current_cell.objects.append(selected_unit)

            if not object_in_cell(cells[move.selected_unit_pos[0]]
                                  [move.selected_unit_pos[1]], Road):
                selected_unit.steps -= 1
            if selected_unit.steps > 0:
                selected_unit.create_unit_pointers(current_cell, selected_unit)
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
        elif ((len(current_cell.objects) > 1 and not isinstance(current_cell.objects[0], Road)) or
              (len(current_cell.objects) > 2 and isinstance(current_cell.objects[0], Road))):
            if hasattr(selected_unit, "attack"):
                from battle.objects.units import SwordsMan, Builder
                from battle.objects.buildings import Fortress, Mine
                enemy = current_cell.objects[-2]
                if (
                    isinstance(enemy, SwordsMan)
                    or isinstance(enemy, Builder)
                    or isinstance(enemy, Fortress)
                    or isinstance(enemy, Mine)
                ):
                    selected_unit.attack(current_cell, selected_unit.player.user_id)
                    await ws.send_command({
                        "action": "attack",
                        "data": {
                            "x": current_cell.j,
                            "y": current_cell.i,
                            "el": len(cells[current_cell.j][current_cell.i].objects) - 2,
                            "damage": selected_unit.damage,
                        }
                    })
                    if isinstance(enemy, Fortress) and enemy.health < 0:
                        await ws.send_command({
                            "action": "win",
                        })
