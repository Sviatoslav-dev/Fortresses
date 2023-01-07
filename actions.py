from objects.units import Builder


def buy_builder(player, cells):
    builder_price = 20
    if player.gold >= builder_price:
        player.gold -= builder_price
        cells[player.fortress_pos[0]][player.fortress_pos[1]].objects.append(
            Builder(player)
        )