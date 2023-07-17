def buy_builder(player, cells):
    from battle.objects.units import Builder
    builder_price = 20
    if player.gold >= builder_price:
        player.gold -= builder_price
        cells[player.fortress_pos[0]][player.fortress_pos[1]].objects.append(
            Builder(player)
        )


def buy_swordsman(player, cells):
    from battle.objects.units import SwordsMan
    swordsman_price = 20
    if player.gold >= swordsman_price:
        player.gold -= swordsman_price
        cells[player.fortress_pos[0]][player.fortress_pos[1]].objects.append(
            SwordsMan(player)
        )
