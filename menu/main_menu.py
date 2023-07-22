import asyncio
import json
from tkinter import *

import requests

from battle.main import main

window = Tk()


def update_units_data(widgets):
    units_data = get_units_data()

    for unit_name in widgets.keys():
        for char in widgets[unit_name].keys():
            widgets[unit_name][char]["price"].set(units_data[unit_name][char])
            widgets[unit_name][char]["update_price"].set(units_data[unit_name][char + '_update_price'])


def send_update_unit_command(unit_type, skill, wgts):
    def f():
        print("CLICK")
        requests.get(
            f'http://127.0.0.1:8000/update_unit?user_id={70}&unit_type={unit_type}&skill={skill}')
        update_units_data(wgts)

    window.children.clear()
    return f


def get_units_data():
    response = requests.get('http://127.0.0.1:8000/player_units/')
    print(response.text)
    return json.loads(response.text)


def start_battle():
    global window
    window.destroy()
    asyncio.run(main())


def create_characteristic_info(unit_name, name, unit, y, wind, wgts):
    widgets = {}

    lbl_text = StringVar(wind)
    lbl_text.set(str(unit[name]))
    lbl = Label(wind, textvariable=lbl_text, fg='red', font=("Helvetica", 10))
    lbl.place(x=400, y=y)
    widgets["price"] = lbl_text

    btn_text = StringVar(wind)
    btn_text.set(str(unit[name + '_update_price']))
    btn = Button(wind, textvariable=btn_text, fg='blue',
                 command=send_update_unit_command(unit_name, name, wgts))
    btn.place(x=450, y=y)
    widgets["update_price"] = btn_text
    return widgets


def create_unit_info(name, units_data, y, wind, wgts):
    chars = units_data[name]
    sm_label = Label(wind, text=name, fg='red', font=("Helvetica", 16))
    sm_label.place(x=50, y=y)

    widgets = {}
    for char, ch_y in zip(["damage", "heath"], [y-20, y+20]):
        widgets[char] = create_characteristic_info(name, char, chars, ch_y, wind, wgts)
    return widgets


def open_shop():
    global window
    shop_window = Tk()
    shop_window.geometry("800x600+500+200")
    lbl = Label(shop_window, text="Shop", fg='red', font=("Helvetica", 16))
    lbl.place(x=350, y=200)

    units_data = get_units_data()

    wgts = {}
    for unit_name, y in zip(list(units_data.keys())[1:], range(300, (len(units_data)-1) * 300, 100)):
        wgts[unit_name] = create_unit_info(unit_name, units_data, y, shop_window, wgts)

    update_units_data(wgts)

    shop_window.mainloop()


if __name__ == '__main__':
    lbl = Label(window, text="Start Game", fg='red', font=("Helvetica", 16))
    lbl.place(x=350, y=200)
    btn = Button(window, text="Start", fg='blue', command=start_battle)
    btn.place(x=350, y=330)
    btn = Button(window, text="Shop", fg='blue', command=open_shop)
    btn.place(x=350, y=370)
    window.title('Hello Python')
    window.geometry("800x600+500+200")
    window.mainloop()
