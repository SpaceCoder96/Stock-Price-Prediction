from tkinter import *
from tkinter.font import Font
from subprocess import call
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
import os.path
import os
import pandas
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd
import csv

news_csv_file = os.path.isfile(r'assets/usr/news.csv')
if news_csv_file == True:
    os.remove(r'assets/usr/news.csv')
else:
    pass

def make():
    ticker = str(ticker_ID_Entry_stock_predictor_input.get())
    ticker_ID = str(ticker)
    news_tables = {}
    finviz_url = 'https://finviz.com/quote.ashx?t='
    ticker = str(ticker_ID)

    url = finviz_url + ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response, 'html')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

    web_data = news_tables[ticker]
    web_data_rows = web_data.findAll('tr')

    parse = []

    for ticker, news_table in news_tables.items():
        for row in news_table.findAll('tr'):
            web_title = row.a.get_text()
            web_date_data = row.td.text.split(' ')
            if len(web_date_data) == 1:
                time = web_date_data[0]
            else:
                date = web_date_data[0]
                time = web_date_data[1]
            parse.append([web_title])

    web_df = pd.DataFrame(parse, columns=['title'])
    web_df.to_csv(r'assets/usr/news.csv', header=False, index=False)
    root.destroy()
    call(['python', 'News Output.py'])

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

background_image_login = Image.open(r"assets\Background\news_input_bg.png")
background_resized_login = background_image_login.resize((1534, 860), Image.ANTIALIAS)
background_new_image_login = ImageTk.PhotoImage(background_resized_login)

quit_btn = Image.open("assets\Buttons\quit_btn_light.png")
quit_btn_resized = quit_btn.resize((54, 89), Image.ANTIALIAS)
quit_btn_new = ImageTk.PhotoImage(quit_btn_resized)

find_btn_inactive = Image.open(r"assets\Buttons\find_btn_inactive.png")
find_btn_inactive_resized = find_btn_inactive.resize((311, 74), Image.ANTIALIAS)
find_btn_inactive_new = ImageTk.PhotoImage(find_btn_inactive_resized)

find_btn_active = Image.open(r"assets\Buttons\find_btn_active.png")
find_btn_active_resized = find_btn_active.resize((311, 74), Image.ANTIALIAS)
find_btn_active_new = ImageTk.PhotoImage(find_btn_active_resized)

def press():
    root.destroy()

def find_enter(event):
    find_button.config(image=find_btn_active_new)

def find_exit(event):
    find_button.config(image=find_btn_inactive_new)

Background_Label = Label(root, image=background_new_image_login)
Background_Label.pack(fill=BOTH)

quit_button = Button(Background_Label, image=quit_btn_new, bd=0, relief='sunken', bg='#D1E4FB', activebackground='#D1E4FB', command=press, highlightbackground='#D1E4FB')
quit_button.place(x=1460, y=-1)

ticker_ID_Entry_stock_predictor_input = Entry(root, font=Font2, relief="groove", highlightbackground="#0047AB", highlightcolor="#0047AB", highlightthickness=2, fg="#17224E", bg='#D1E4FB')
ticker_ID_Entry_stock_predictor_input.place(x=575, y=400)

find_button = Button(Background_Label, image=find_btn_inactive_new, bd=0, relief='sunken', bg='#17224E', activebackground='#17224E', highlightbackground='#17224E', command=make)
find_button.place(x=600, y=490)

find_button.bind('<Enter>', find_enter)
find_button.bind('<Leave>', find_exit)

root.mainloop()