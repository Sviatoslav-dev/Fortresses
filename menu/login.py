import os
import json
from tkinter import *

import requests

from menu.main_menu import main_menu


def send_login(name, password, wind):
    res = requests.post(f'http://127.0.0.1:8000/login', json={
        "login": name,
        "password": password
    })
    print(res.text)
    if res.status_code == 200:
        user_id = json.loads(res.text)["id"]
        if user_id:
            wind.destroy()
            main_menu(int(user_id))
    lbl = Label(wind, text="Incorrect login or password", fg='red', font=("Helvetica", 8), bg='#ddf0e0')
    lbl.place(relx=0.5, rely=0.7, anchor=CENTER)


def send_register(name, password, wind):
    if password != "" and name != "":
        res = requests.post(f'http://127.0.0.1:8000/register', json={
            "login": name,
            "password": password
        })
        print(res.text)
        if res.status_code == 200:
            wind.destroy()
            main_menu(int(json.loads(res.text)["id"]))
    else:
        lbl = Label(wind, text="Login and password must be filled", fg='red', font=("Helvetica", 8),
                    bg='#ddf0e0')
        lbl.place(relx=0.5, rely=0.7, anchor=CENTER)


def do_login(log_btn, pass_btn, wind):
    def f():
        send_login(log_btn.get(), pass_btn.get(), wind)

    return f


def do_register(log_btn, pass_btn, wind):
    def f():
        send_register(log_btn.get(), pass_btn.get(), wind)

    return f


def go_to_login(wind):
    def f():
        wind.destroy()
        login()

    return f


def go_to_register(wind):
    def f():
        wind.destroy()
        register()

    return f


def register():
    window = Tk()
    bg_color = '#ddf0e0'
    window.configure(bg=bg_color)
    lbl = Label(window, text="Register", fg='#4a5157', font=("Helvetica", 32), bg=bg_color)
    lbl.place(relx=0.5, rely=0.3, anchor=CENTER)

    login_lbl = Label(window, text="name", fg='#4a5157', font=("Helvetica", 10), bg=bg_color)
    login_lbl.place(relx=0.42, rely=0.5, anchor=E)
    login_txt = Entry(window, width=20)
    login_txt.place(relx=0.5, rely=0.5, anchor=CENTER)
    pass_lbl = Label(window, text="password", fg='#4a5157', font=("Helvetica", 10), bg=bg_color)
    pass_lbl.place(relx=0.42, rely=0.55, anchor=E)
    password_txt = Entry(window, width=20, show="*")
    password_txt.place(relx=0.5, rely=0.55, anchor=CENTER)
    login_btn = Button(window, text="Register", fg='#271c1b', command=do_register(login_txt,
                                                                            password_txt, window),
                       bg="#a2b7b2", width=10, border="0")
    login_btn.place(relx=0.5, rely=0.6, anchor=CENTER)
    login_btn = Button(window, text="Login", fg='#271c1b', command=go_to_login(window),
                       bg="#a2b7b2", width=10, border="0")
    login_btn.place(relx=0.5, rely=0.65, anchor=CENTER)
    window.title('Fortresses')
    window.geometry("800x600+500+200")
    window.mainloop()


def login():
    window = Tk()
    bg_color = '#ddf0e0'
    window.configure(bg=bg_color)
    lbl = Label(window, text="Login", fg='#4a5157', font=("Helvetica", 32), bg=bg_color)
    lbl.place(relx=0.5, rely=0.3, anchor=CENTER)

    login_lbl = Label(window, text="name", fg='#4a5157', font=("Helvetica", 10), bg=bg_color)
    login_lbl.place(relx=0.42, rely=0.5, anchor=E)
    login_txt = Entry(window, width=20)
    login_txt.place(relx=0.5, rely=0.5, anchor=CENTER)
    pass_lbl = Label(window, text="password", fg='#4a5157', font=("Helvetica", 10), bg=bg_color)
    pass_lbl.place(relx=0.42, rely=0.55, anchor=E)
    password_txt = Entry(window, width=20, show="*")
    password_txt.place(relx=0.5, rely=0.55, anchor=CENTER)
    login_btn = Button(window, text="Login", fg='#271c1b', command=do_login(login_txt,
                                                                      password_txt, window),
                 bg="#a2b7b2", width=10, border="0")
    login_btn.place(relx=0.5, rely=0.6, anchor=CENTER)
    login_btn = Button(window, text="Register", fg='#271c1b', command=go_to_register(window),
                       bg="#a2b7b2", width=10, border="0")
    login_btn.place(relx=0.5, rely=0.65, anchor=CENTER)
    window.title('Fortresses')
    window.geometry("800x600+500+200")
    window.mainloop()


if __name__ == '__main__':
    login()
