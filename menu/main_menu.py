import asyncio
from tkinter import *

from battle.main import main

window = Tk()


def start_battle():
    global window
    window.destroy()
    asyncio.run(main())


lbl = Label(window, text="Start Game", fg='red', font=("Helvetica", 16))
lbl.place(x=350, y=200)
btn = Button(window, text="Start", fg='blue', command=start_battle)
btn.place(x=350, y=330)
window.title('Hello Python')
window.geometry("800x600+500+600")
window.mainloop()
