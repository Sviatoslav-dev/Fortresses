import asyncio
import json
from tkinter import *

import requests

from battle.main import main


def update_units_data(widgets, user_id):
    units_data = get_units_data(user_id)

    for unit_name in widgets.keys():
        for char in widgets[unit_name].keys():
            widgets[unit_name][char]["price"].set(units_data[unit_name][char])
            widgets[unit_name][char]["update_price"].set(
                units_data[unit_name][char + '_update_price'])


def send_update_unit_command(unit_type, skill, wgts, user_id):
    def f():
        print("CLICK")
        requests.get(
            f'http://127.0.0.1:8000/update_unit?user_id={user_id}&unit_type={unit_type}&skill={skill}')
        update_units_data(wgts, user_id)

    return f


def send_open_unit(unit_type, wind, user_id):
    def f():
        print("CLICK")
        requests.get(f'http://127.0.0.1:8000/open_unit?user_id={user_id}&unit_type={unit_type}')
        wind.destroy()
        open_shop(wind, user_id)

    return f


def get_units_data(user_id):
    response = requests.get(f'http://127.0.0.1:8000/player_units?user_id={user_id}')
    print(response.text)
    return json.loads(response.text)


def start_battle(window):
    def f():
        window.destroy()
        asyncio.run(main())
    return f


def create_characteristic_info(unit_name, name, unit, y, wind, wgts, user_id):
    widgets = {}

    lbl_text = StringVar(wind)
    lbl_text.set(str(unit[name]))
    lbl = Label(wind, textvariable=lbl_text, fg='red', font=("Helvetica", 10))
    lbl.place(x=400, y=y)
    widgets["price"] = lbl_text

    btn_text = StringVar(wind)
    btn_text.set(str(unit[name + '_update_price']))
    btn = Button(wind, textvariable=btn_text, fg='blue',
                 command=send_update_unit_command(unit_name, name, wgts, user_id))
    btn.place(x=450, y=y)
    widgets["update_price"] = btn_text
    return widgets


def create_unit_info(name, units_data, y, wind, wgts, user_id):
    chars = units_data[name]
    sm_label = Label(wind, text=name, fg='red', font=("Helvetica", 16))
    sm_label.place(x=50, y=y)

    widgets = {}
    for char, ch_y in zip(["damage", "heath"], [y - 20, y + 20]):
        widgets[char] = create_characteristic_info(name, char, chars, ch_y, wind, wgts, user_id)
    return widgets


def create_open_button(wind, y, unit_name, user_id):
    sm_label = Label(wind, text=unit_name, fg='red', font=("Helvetica", 16))
    sm_label.place(x=50, y=y)

    btn = Button(wind, text="50", fg='blue', command=send_open_unit(unit_name, wind, user_id))
    btn.place(x=450, y=y)


def open_shop(window, user_id):
    def f():
        try:
            window.destroy()
        except TclError:
            pass
        shop_window = Tk()
        shop_window.geometry("800x600+500+200")
        lbl = Label(shop_window, text="Shop", fg='red', font=("Helvetica", 16))
        lbl.place(x=350, y=200)

        units_data = get_units_data(user_id)

        wgts = {}
        for unit_name, y in zip(list(units_data.keys())[1:],
                                range(300, (len(units_data) - 1) * 300, 100)):
            if units_data[unit_name]["opened"]:
                wgts[unit_name] = create_unit_info(unit_name, units_data, y, shop_window, wgts, user_id)
            else:
                create_open_button(shop_window, y, unit_name, user_id)

        update_units_data(wgts, user_id)

        shop_window.mainloop()
    return f


def main_menu(user_id):
    window = Tk()
    lbl = Label(window, text="Start Game", fg='red', font=("Helvetica", 16))
    lbl.place(x=350, y=200)
    btn = Button(window, text="Start", fg='blue', command=start_battle(window))
    btn.place(x=350, y=330)
    btn = Button(window, text="Shop", fg='blue', command=open_shop(window, user_id))
    btn.place(x=350, y=370)
    window.title('Hello Python')
    window.geometry("800x600+500+200")
    window.mainloop()


if __name__ == '__main__':
    main_menu(70)
