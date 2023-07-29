def buy_builder(player, cells):
    from battle.objects.units import Builder
    builder_price = player.units_data["builder"]["gold_price"]
    if player.gold >= builder_price:
        player.gold -= builder_price
        cells[player.fortress_pos[0]][player.fortress_pos[1]].objects.append(
            Builder(player)
        )


def buy_swordsman(player, cells):
    from battle.objects.units import SwordsMan
    swordsman_price = player.units_data["swordsman"]["gold_price"]
    if player.gold >= swordsman_price:
        player.gold -= swordsman_price
        cells[player.fortress_pos[0]][player.fortress_pos[1]].objects.append(
            SwordsMan(player)
        )


def buy_road(player, cells, j, i):
    from battle.objects.buildings import Road
    road_price = 20
    if player.gold >= road_price:
        player.gold -= road_price
        cells[j][i].objects.insert(
            -2, Road(player),
        )


def buy_mine(player, cells, j, i):
    from battle.objects.buildings import Mine
    road_price = 20
    if player.gold >= road_price:
        player.gold -= road_price
        cells[j][i].objects.insert(
            -2, Mine(player),
        )
