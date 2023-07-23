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
        wind.destroy()
        main_menu(int(json.loads(res.text)["id"]))


def do_login(log_btn, pass_btn, wind):
    def f():
        send_login(log_btn.get(1.0, "end-1c"), pass_btn.get(1.0, "end-1c"), wind)

    return f


def login():
    window = Tk()
    lbl = Label(window, text="Login", fg='red', font=("Helvetica", 16))
    lbl.place(x=350, y=200)

    login_txt = Text(window, height=1, width=20)
    login_txt.place(x=350, y=300)
    password_txt = Text(window, height=1, width=20)
    password_txt.place(x=350, y=320)
    login_btn = Button(window, text="Start", fg='blue', command=do_login(login_txt,
                                                                         password_txt, window))
    login_btn.place(x=350, y=360)
    window.title('Hello Python')
    window.geometry("800x600+500+200")
    window.mainloop()


if __name__ == '__main__':
    login()
