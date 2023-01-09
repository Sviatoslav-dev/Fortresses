import asyncio
import json
from tkinter import *

import requests

from battle.main import main

window = Tk()


def send_update_unit_command(unit_type, skill):
    def f():
        requests.get(f'http://127.0.0.1:8001/update_unit?user_id={1}&unit_type={unit_type}&skill={skill}')
    return f


def get_units_data():
    return json.loads(requests.get('http://127.0.0.1:8001/player_units/').text)


def start_battle():
    global window
    window.destroy()
    asyncio.run(main())


def open_shop():
    global window
    shop_window = Tk()
    shop_window.geometry("800x600+500+200")
    lbl = Label(shop_window, text="Shop", fg='red', font=("Helvetica", 16))
    lbl.place(x=350, y=200)

    units_data = get_units_data()

    sm_label = Label(shop_window, text="Swordsman", fg='red', font=("Helvetica", 16))
    sm_label.place(x=50, y=300)

    sm_damage_lbl = Label(shop_window, text=str(units_data["swordsman"]["damage"]), fg='red', font=("Helvetica", 10))
    sm_damage_lbl.place(x=400, y=280)
    sm_damage_btn = Button(shop_window, text=str(units_data["swordsman"]["damage_update_price"]), fg='blue',
                           command=send_update_unit_command("swordsman", "damage"))
    sm_damage_btn.place(x=450, y=280)

    sm_heath_lbl = Label(shop_window, text=str(units_data["swordsman"]["heath"]), fg='red', font=("Helvetica", 10))
    sm_heath_lbl.place(x=400, y=320)
    sm_heath_btn = Button(shop_window, text=str(units_data["swordsman"]["heath_update_price"]), fg='blue',
                          command=send_update_unit_command("swordsman", "heath"))
    sm_heath_btn.place(x=450, y=320)

    archer_label = Label(shop_window, text="Archer", fg='red', font=("Helvetica", 16))
    archer_label.place(x=50, y=400)

    archer_damage_lbl = Label(shop_window, text=str(units_data["archer"]["damage"]), fg='red', font=("Helvetica", 10))
    archer_damage_lbl.place(x=400, y=380)
    archer_damage_btn = Button(shop_window, text=str(units_data["archer"]["damage_update_price"]), fg='blue',
                               command=send_update_unit_command("archer", "damage"))
    archer_damage_btn.place(x=450, y=380)

    archer_heath_lbl = Label(shop_window, text=str(units_data["archer"]["heath"]), fg='red', font=("Helvetica", 10))
    archer_heath_lbl.place(x=400, y=420)
    archer_heath_btn = Button(shop_window, text=str(units_data["archer"]["heath_update_price"]), fg='blue',
                              command=send_update_unit_command("archer", "heath"))
    archer_heath_btn.place(x=450, y=420)

    shop_window.mainloop()


lbl = Label(window, text="Start Game", fg='red', font=("Helvetica", 16))
lbl.place(x=350, y=200)
btn = Button(window, text="Start", fg='blue', command=start_battle)
btn.place(x=350, y=330)
btn = Button(window, text="Shop", fg='blue', command=open_shop)
btn.place(x=350, y=370)
window.title('Hello Python')
window.geometry("800x600+500+200")
window.mainloop()
