from tkinter import *
from tkinter.font import Font
from subprocess import call
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
import os.path
import os

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

background_image_login = Image.open("assets\Background\Options_bg.png")
background_resized_login = background_image_login.resize((1534, 860), Image.ANTIALIAS)
background_new_image_login = ImageTk.PhotoImage(background_resized_login)

quit_btn = Image.open("assets\Buttons\quit_btn_light.png")
quit_btn_resized = quit_btn.resize((54, 89), Image.ANTIALIAS)
quit_btn_new = ImageTk.PhotoImage(quit_btn_resized)

stock_predictor_btn_inactive = Image.open("assets\Buttons\stock_predictor_btn_inactive.png")
stock_predictor_btn_inactive_resized = stock_predictor_btn_inactive.resize((450, 94), Image.ANTIALIAS)
stock_predictor_btn_inactive_new = ImageTk.PhotoImage(stock_predictor_btn_inactive_resized)

stock_predictor_btn_active = Image.open("assets\Buttons\stock_predictor_btn_active.png")
stock_predictor_btn_active_resized = stock_predictor_btn_active.resize((450, 94), Image.ANTIALIAS)
stock_predictor_btn_active_new = ImageTk.PhotoImage(stock_predictor_btn_active_resized)

stock_news_btn_inactive = Image.open("assets\Buttons\stock_news_btn_inactive.png")
stock_news_btn_inactive_resized = stock_news_btn_inactive.resize((450, 94), Image.ANTIALIAS)
stock_news_btn_inactive_new = ImageTk.PhotoImage(stock_news_btn_inactive_resized)

stock_news_btn_active = Image.open("assets\Buttons\stock_news_btn_active.png")
stock_news_btn_active_resized = stock_news_btn_active.resize((450, 94), Image.ANTIALIAS)
stock_news_btn_active_new = ImageTk.PhotoImage(stock_news_btn_active_resized)

def stock_predictor_enter(event):
    stock_predictor_button.config(image=stock_predictor_btn_active_new)

def stock_predictor_exit(event):
    stock_predictor_button.config(image=stock_predictor_btn_inactive_new)

def stock_news_enter(event):
    stock_news_button.config(image=stock_news_btn_active_new)

def stock_news_exit(event):
    stock_news_button.config(image=stock_news_btn_inactive_new)

def press():
    root.destroy()

def stock_prediction():
    root.destroy()
    call(['python', 'Stock Predictor Input.py'])

def stock_portfolio():
    root.destroy()
    call(['python', 'Stock Portfolio.py'])

def news():
    root.destroy()
    call(['python', r'News Input.py'])

def candlestick():
    root.destroy()
    call(['python', 'Candlestick Input.py'])

Background_Label = Label(root, image=background_new_image_login)
Background_Label.pack(fill=BOTH)

quit_button = Button(Background_Label, image=quit_btn_new, bd=0, relief='sunken', bg='#D1E4FB', activebackground='#D1E4FB', command=press, highlightbackground='#D1E4FB')
quit_button.place(x=1460, y=-1)

stock_predictor_button = Button(Background_Label, image=stock_predictor_btn_inactive_new, bd=0, relief='sunken', bg='#17224E', activebackground='#17224E', highlightbackground='#17224E', command=stock_prediction)
stock_predictor_button.place(x=0, y=300)

stock_predictor_button.bind('<Enter>', stock_predictor_enter)
stock_predictor_button.bind('<Leave>', stock_predictor_exit)

stock_news_button = Button(Background_Label, image=stock_news_btn_inactive_new, bd=0, relief='sunken', bg='#17224E', activebackground='#17224E', highlightbackground='#17224E', command=news)
stock_news_button.place(x=0, y=500)

stock_news_button.bind('<Enter>', stock_news_enter)
stock_news_button.bind('<Leave>', stock_news_exit)

root.mainloop()