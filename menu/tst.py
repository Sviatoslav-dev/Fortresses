from tkinter import *
import time
from threading import *

DoLoading = False


def dow():
    global DoLoading
    while DoLoading:
        window_w.title("Загрузка.")
        time.sleep(1)
        window_w.title("Загрузка..")
        time.sleep(1)
        window_w.title("Загрузка...")
        time.sleep(1)
        window_w.title("Загрузка....")
        time.sleep(1)
    window_w.title("Готов")


def loading():
    global DoLoading
    DoLoading = True
    Thread(target=dow).start()


def loading_stop():
    global DoLoading
    DoLoading = False
    vls = window.children
    window.destroy()
    # time.sleep(5)
    window.pack(fill="both", expand=True)


window_w = Tk()
window = Frame(window_w)
window_w.geometry('600x450')
window_w.resizable(width=False, height=False)
btn = Button(window, text="Готово", command=loading_stop)
btn.nametowidget(name=btn)
btn.grid(column=1, row=0)

window.pack(fill="both", expand=True)

loading()
window.mainloop()
