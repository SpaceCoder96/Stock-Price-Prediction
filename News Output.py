from tkinter import *
from tkinter.font import Font
from subprocess import call
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
import os.path
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd
import csv
from tkinter import ttk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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

Font3 = Font(
    family="Arial",
    size=15
)

def find():
    file = open(r'assets/usr/news.csv')
    reader = csv.reader(file)
    imported_data = list(reader)
    imported_data_list = []
    for item in list(range(0, len(imported_data))):
        imported_data_list.append(imported_data[item][0])
    for x, y in enumerate(imported_data_list):
        vader = SentimentIntensityAnalyzer()
        score = vader.polarity_scores(y)
        final = score['compound']
        z = float(final)
        table.insert('', 'end', values=(x+1, y, z))

background_image_login = Image.open(r"assets\Background\news_output_bg.png")
background_resized_login = background_image_login.resize((1534, 860), Image.ANTIALIAS)
background_new_image_login = ImageTk.PhotoImage(background_resized_login)

quit_btn = Image.open("assets\Buttons\quit_btn_light.png")
quit_btn_resized = quit_btn.resize((54, 89), Image.ANTIALIAS)
quit_btn_new = ImageTk.PhotoImage(quit_btn_resized)

def press():
    root.destroy()

Background_Label = Label(root, image=background_new_image_login)
Background_Label.pack(fill=BOTH)

quit_button = Button(Background_Label, image=quit_btn_new, bd=0, relief='sunken', bg='#D1E4FB', activebackground='#D1E4FB', command=press, highlightbackground='#D1E4FB')
quit_button.place(x=1460, y=-1)

Frame1 = Frame(Background_Label, bg='white')
Frame1.place(x=175, y=150, width=1200, height=575)

scrollbar = Scrollbar(Frame1, orient='vertical')
scrollbar.pack(side=RIGHT, fill=Y)
ttk.Style().configure('Treeview', background='white', foreground='#17224E', font=Font3, rowheight=30, fieldbackground='white')
ttk.Style().map('Treeview', background=[('selected', '#17224E')], foreground=[('selected', 'white')])
table = ttk.Treeview(Frame1, columns=(1, 2, 3), show='headings', height=28, selectmode='extended')
table.pack(expand=YES, fill=BOTH)
table.configure(yscrollcommand=scrollbar.set, selectmode='browse')
table.column('#1', width=50, anchor=CENTER, stretch=NO)
table.column('#3', width=100, anchor=CENTER, stretch=NO)
table.heading(1, text='SR. NO.')
table.heading(2, text='NEWS')
table.heading(3, text='SCORE')

find()

root.mainloop()