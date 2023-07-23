from tkinter import *
import time
from threading import *

DoLoading = False


def dow():
    global DoLoading
    while DoLoading:
        window.title("Загрузка.")
        time.sleep(1)
        window.title("Загрузка..")
        time.sleep(1)
        window.title("Загрузка...")
        time.sleep(1)
        window.title("Загрузка....")
        time.sleep(1)
    window.title("Готов")


def loading():
    global DoLoading
    DoLoading = True
    Thread(target=dow).start()


def loading_stop():
    global DoLoading
    DoLoading = False
    window.destroy()


window = Tk()
window.geometry('600x450')
window.resizable(width=False, height=False)
btn = Button(window, text="Готово", command=loading_stop)
btn.nametowidget(name=btn)
btn.grid(column=1, row=0)

loading()
window.mainloop()
