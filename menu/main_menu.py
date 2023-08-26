import os
# os.chdir('..')

from PIL import Image, ImageTk
import asyncio
import json
import tkinter as tk

import requests

from battle.main import main


def update_units_data(widgets, user_id):
    user_data = get_user_data(user_id)
    units_data = get_units_data(user_id)

    for unit_name in widgets.keys():
        if unit_name != "stars":
            for char in widgets[unit_name].keys():
                widgets[unit_name][char]["price"].set(char + ": " + str(units_data[unit_name][char]))
                widgets[unit_name][char]["update_price"].set(
                    units_data[unit_name][char + '_update_price'])
    widgets["stars"].set(user_data["stars"])


def send_update_unit_command(unit_type, skill, wgts, user_id):
    def f():
        print("CLICK")
        requests.get(
            f'http://127.0.0.1:8000/update_unit?user_id={user_id}&unit_type={unit_type}&skill={skill}')
        update_units_data(wgts, user_id)

    return f


def send_open_unit(unit_type, wind, user_id, stars):
    def f():
        requests.get(f'http://127.0.0.1:8000/open_unit?user_id={user_id}&unit_type={unit_type}')
        open_shop(wind, user_id, stars)()

    return f


def get_units_data(user_id):
    response = requests.get(f'http://127.0.0.1:8000/player_units?user_id={user_id}')
    return json.loads(response.text)


def get_user_data(user_id):
    response = requests.get(f'http://127.0.0.1:8000/user?user_id={user_id}')
    return json.loads(response.text)


def start_battle(window, user_id):
    def f():
        window.destroy()
        asyncio.run(main(user_id))
        main_menu(user_id)

    return f


def create_characteristic_info(unit_name, name, unit, y, wind, wgts, user_id):
    star_img = Image.open("menu/icons/star.png")
    star_img = star_img.resize((50, 50))
    star = ImageTk.PhotoImage(star_img)

    bg_color = '#ddf0e0'
    widgets = {}

    lbl_text = tk.StringVar(wind)
    lbl_text.set(str(unit[name]))
    lbl = tk.Label(wind, textvariable=lbl_text, fg='#4a5157', font=("Helvetica", 10), bg=bg_color)
    lbl.place(x=300, y=y)
    widgets["price"] = lbl_text

    btn_text = tk.StringVar(wind)
    btn_text.set(str(unit[name + '_update_price']))
    btn = tk.Button(wind, textvariable=btn_text, fg='#271c1b',
                 command=send_update_unit_command(unit_name, name, wgts, user_id), width=5, border="0", bg="#a2b7b2")
    btn.place(x=450, y=y)
    widgets["update_price"] = btn_text
    return widgets


def create_unit_info(name, units_data, y, wind, wgts, user_id):
    chars = units_data[name]
    bg_color = '#ddf0e0'
    sm_label = tk.Label(wind, text=name, fg='#4a5157', font=("Helvetica", 16), bg=bg_color)
    sm_label.place(x=50, y=y)

    widgets = {}
    for char, ch_y in zip(["damage", "heath"], [y - 20, y + 20]):
        widgets[char] = create_characteristic_info(name, char, chars, ch_y, wind, wgts, user_id)
    return widgets


def create_open_button(wind, y, unit_name, user_id, stars):
    bg_color = '#ddf0e0'
    sm_label = tk.Label(wind, text=unit_name, fg='#4a5157', font=("Helvetica", 16), bg=bg_color)
    sm_label.place(x=50, y=y)

    sm_label = tk.Label(wind, text="closed", fg='#4a5157', font=("Helvetica", 16), bg=bg_color)
    sm_label.place(x=300, y=y)

    btn = tk.Button(wind, text="50", fg='#271c1b', command=send_open_unit(unit_name, wind, user_id,
                                                                          stars),
                    width=5, border="0", bg="#a2b7b2")
    btn.place(x=450, y=y)

    # stars_lbl = tk.Label(wind, image=star)
    # stars_lbl.place(relx=0.56, rely=0.5, anchor=tk.CENTER)
    # stars_lbl.place(x=460, y=y)


def open_main_menu(wind, user_id):
    def f():
        wind.destroy()
        main_menu(user_id)

    return f


def open_shop(window, user_id, stars):
    def f():
        try:
            window.destroy()
        except tk.TclError:
            pass
        shop_window = tk.Tk()
        bg_color = '#ddf0e0'
        shop_window.configure(bg=bg_color)
        shop_window.geometry("800x600+500+200")

        btn = tk.Button(shop_window, text="<-", fg='#4a5157',
                        command=open_main_menu(shop_window, user_id),
                        width=5, border="0", bg="#a2b7b2")
        btn.place(x=10, y=10)

        star_img = Image.open("menu/icons/star.png")
        star_img = star_img.resize((50, 50))
        star = ImageTk.PhotoImage(star_img)

        star_lbl = tk.Label(shop_window, image=star, bg=bg_color)
        star_lbl.place(relx=0.56, rely=0.05, anchor=tk.CENTER)
        stars_text = tk.StringVar(shop_window)
        stars_text.set(str(stars))
        stars_lbl = tk.Label(shop_window, textvariable=stars_text, fg='#271c1b', font=("Helvetica", 12),
                             bg=bg_color)
        stars_lbl.place(relx=0.6, rely=0.05, anchor=tk.CENTER)

        lbl = tk.Label(shop_window, text="Shop", fg='#4a5157', font=("Helvetica", 16), bg=bg_color)
        lbl.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        units_data = get_units_data(user_id)

        wgts = {}
        wgts["stars"] = stars_text
        for unit_name, y in zip(list(units_data.keys())[1:],
                                range(300, (len(units_data) - 1) * 300, 100)):
            if units_data[unit_name]["opened"]:
                wgts[unit_name] = create_unit_info(unit_name, units_data, y, shop_window, wgts,
                                                   user_id)
            else:
                create_open_button(shop_window, y, unit_name, user_id, stars)

        update_units_data(wgts, user_id)

        shop_window.mainloop()

    return f


def main_menu(user_id):
    window = tk.Tk()
    bg_color = '#ddf0e0'
    window.configure(bg=bg_color)
    user_data = get_user_data(user_id)
    star_img = Image.open("menu/icons/star.png")
    star_img = star_img.resize((50, 50))
    star = ImageTk.PhotoImage(star_img)

    cup_img = Image.open("menu/icons/cup.png")
    cup_img = cup_img.resize((50, 50))
    cup = ImageTk.PhotoImage(cup_img)

    cup_lbl = tk.Label(window, image=cup, bg=bg_color)
    cup_lbl.place(relx=0.36, rely=0.05, anchor=tk.CENTER)
    rating = tk.Label(window, text=str(user_data["rating"]), fg='#271c1b', font=("Helvetica", 12), bg=bg_color)
    rating.place(relx=0.4, rely=0.05, anchor=tk.CENTER)

    stars_lbl = tk.Label(window, image=star, bg=bg_color)
    stars_lbl.place(relx=0.56, rely=0.05, anchor=tk.CENTER)
    stars = tk.Label(window, text=str(user_data["stars"]), fg='#271c1b', font=("Helvetica", 12), bg=bg_color)
    stars.place(relx=0.6, rely=0.05, anchor=tk.CENTER)

    lbl = tk.Label(window, text="Fortresses", fg='#4a5157', font=("Helvetica", 32), bg=bg_color)
    lbl.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    lbl = tk.Label(window, text=user_data["name"], fg='#4a5157', font=("Helvetica", 12), bg=bg_color)
    lbl.place(x=5, y=5)
    btn = tk.Button(window, text="Start", fg='#271c1b', command=start_battle(window, user_id), bg="#a2b7b2", width=10, border="0")
    btn.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    btn = tk.Button(window, text="Shop", fg='#271c1b',
                 command=open_shop(window, user_id, user_data["stars"]), bg="#a2b7b2", width=10, border="0")
    btn.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    window.title('Fortresses')
    window.geometry("800x600+500+200")
    window.mainloop()


if __name__ == '__main__':
    main_menu(74)
