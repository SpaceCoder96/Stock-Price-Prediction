from tkinter import *
from tkinter.font import Font
from subprocess import call
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
import os.path
import os
import pickle
import sys

filepath = r"assets\usr\predicted_price.dat"
file = open(filepath, 'rb')
price = pickle.load(file)

root = Tk()
root.title('StocX')
root.attributes('-fullscreen', True)
# root.state('zoomed')
Font1 = Font(
    family="Arial",
    size=40
)

Font2 = Font(
    family="Arial",
    size=25
)

background_image_login = Image.open("assets\Background\stock_predictor_output_bg.png")
background_resized_login = background_image_login.resize((1534, 860), Image.ANTIALIAS)
background_new_image_login = ImageTk.PhotoImage(background_resized_login)

quit_btn = Image.open("assets\Buttons\quit_btn_light.png")
quit_btn_resized = quit_btn.resize((54, 89), Image.ANTIALIAS)
quit_btn_new = ImageTk.PhotoImage(quit_btn_resized)

chart_image_login = Image.open(r"assets\usr\prediction.png")
chart_resized_login = chart_image_login.resize((740, 580), Image.ANTIALIAS)
chart_new_image_login = ImageTk.PhotoImage(chart_resized_login)

def press():
    root.destroy()
    sys.exit()

Background_Label = Label(root, image=background_new_image_login)
Background_Label.pack(fill=BOTH)

quit_button = Button(Background_Label, image=quit_btn_new, bd=0, relief='sunken', bg='#D1E4FB', activebackground='#D1E4FB', command=press, highlightbackground='#D1E4FB')
quit_button.place(x=1460, y=-1)

predicted_price_Entry_stock_predictor_input = Entry(root, font=Font2, bg='#D1E4FB', relief="groove", highlightbackground="#0047AB", highlightcolor="#0047AB", highlightthickness=2, fg="#17224E", width=12)
predicted_price_Entry_stock_predictor_input.place(x=110, y=260)

chart_label = Label(Background_Label, image=chart_new_image_login, bd=0)
chart_label.place(x=600, y=215)

predicted_price_Entry_stock_predictor_input.insert(0, price)

root.mainloop()