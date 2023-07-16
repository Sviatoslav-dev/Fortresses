
def buy_builder(player, cells):
    from battle.objects.units import Builder
    builder_price = 20
    if player.gold >= builder_price:
        player.gold -= builder_price
        cells[player.fortress_pos[0]][player.fortress_pos[1]].objects.append(
            Builder(player)
        )
