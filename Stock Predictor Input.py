from tkinter import *
from tkinter.font import Font
from subprocess import call
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
import os.path
import os
import sqlite3
from datetime import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.python.util.nest import is_mapping
import os
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.util import pr
import threading
import pickle
from subprocess import call
import timeit

filepath = r"assets\usr\predicted_price.dat"
exist = os.path.isfile(filepath)
if exist == False:
    open(filepath, 'x').close()
else:
    os.remove(filepath)

output = open(filepath, 'wb')

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

background_image_login = Image.open("assets\Background\stock_predictor_input_bg.png")
background_resized_login = background_image_login.resize((1534, 860), Image.ANTIALIAS)
background_new_image_login = ImageTk.PhotoImage(background_resized_login)

quit_btn = Image.open("assets\Buttons\quit_btn_light.png")
quit_btn_resized = quit_btn.resize((54, 89), Image.ANTIALIAS)
quit_btn_new = ImageTk.PhotoImage(quit_btn_resized)

find_btn_inactive = Image.open(r"assets\Buttons\find_btn_inactive.png")
find_btn_inactive_resized = find_btn_inactive.resize((351, 94), Image.ANTIALIAS)
find_btn_inactive_new = ImageTk.PhotoImage(find_btn_inactive_resized)

find_btn_active = Image.open(r"assets\Buttons\find_btn_active.png")
find_btn_active_resized = find_btn_active.resize((351, 94), Image.ANTIALIAS)
find_btn_active_new = ImageTk.PhotoImage(find_btn_active_resized)

def make():
    def main_func(ticker, parameter):
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
                parse.append([ticker, date, time, web_title])
        web_df = pd.DataFrame(parse, columns=['ticker', 'date', 'time', 'title'])
        vader = SentimentIntensityAnalyzer()
        lam_fun = lambda title: vader.polarity_scores(title)['compound']
        web_df['compound'] = web_df['title'].apply(lam_fun)
        mean_final = web_df['compound'].mean()
        #####################################################################################################################
        start_date = dt.datetime(2000, 1, 1)
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        end_date = (f"{year}, {month}, {day}")
        past_days = int(30)  
        data = web.DataReader(ticker_ID, "yahoo", start_date, end_date)
        scalar = MinMaxScaler(feature_range=(0,1))
        scaled_data = scalar.fit_transform(data[parameter].values.reshape(-1,1))
        x_train = []
        y_train = []
        for x in range(past_days, len(scaled_data)):
                x_train.append(scaled_data[x-past_days:x, 0])
                y_train.append(scaled_data[x, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))  
        training_model = Sequential()
        training_model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        training_model.add(Dropout(0.2))
        training_model.add(LSTM(units=50, return_sequences=True))
        training_model.add(Dropout(0.2))
        training_model.add(LSTM(units=50))
        training_model.add(Dropout(0.2))
        training_model.add(Dense(units=1))
        training_model.compile(optimizer = 'adam', loss = 'mean_squared_error')
        training_model.fit(x_train, y_train, epochs=30, batch_size=32)
        test_data = web.DataReader(ticker_ID, 'yahoo', start_date, end_date)
        actual_prices = test_data['Close'].values
        total_dataset = pd.concat((data['Close'], test_data[parameter]), axis=0)
        model_input = total_dataset[len(total_dataset) - len(test_data) - past_days:].values
        model_inputs = model_input.reshape(-1, 1)
        model_input = scalar.transform(model_inputs)
        x_test = []
        for x in range(past_days, len(model_input)):
                x_test.append(model_input[x-past_days:x, 0])
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        Predicted_prices = training_model.predict(x_test)
        Predicted_prices = scalar.inverse_transform(Predicted_prices)
        plt.plot(actual_prices, color='black', label=f'Actual {ticker_ID} Price')
        plt.plot(Predicted_prices, color='green', label=f'Predicted {ticker_ID} Price')
        plt.title(f'{ticker_ID} Share Price')
        plt.xlabel('Time')
        plt.ylabel(f'{ticker_ID} Share Price')
        plt.legend()
        plt.savefig(r"assets\usr\prediction.png")
        plt.close()
        quote = web.DataReader(ticker_ID, 'yahoo', start_date, end_date)
        df_scalar = MinMaxScaler(feature_range=(0,1))
        df_scaled_data = df_scalar.fit_transform(data[parameter].values.reshape(-1,1))
        df_x_test = []
        df_x_test.append(df_scaled_data)
        df_x_test = np.array(x_test)
        df_x_test = np.reshape(df_x_test, (df_x_test.shape[0], df_x_test.shape[1], 1))
        predict = training_model.predict(df_x_test)
        predict = df_scalar.inverse_transform(predict)
        count = int(0)
        length = len(predict)
        dataframe_list = []
        while count < length:
                initial = predict[count][0]
                count = count + 1
                dataframe_list.append(initial)
        df = pd.DataFrame(dataframe_list, columns=['price'])
        top = df['price'].nlargest(n=40).mean()
        a = float(top)
        b= float(mean_final)
        c = float(a * b)
        final_price_to_display = a + c
        final_round = round(final_price_to_display, 2)
        print(final_round)
        pickle.dump(final_round, output)
        output.close()
        root.destroy()
        call(['python', 'Stock Predictor Output.py'])
    ticker_ID = str(ticker_ID_Entry_stock_predictor_input.get())
    parameter = str(parameter_stock_predictor_input.get())
    find_button['state'] = DISABLED
    print(timeit.timeit(main_func(ticker_ID, parameter), number=1))


def find_enter(event):
    find_button.config(image=find_btn_active_new)

def find_exit(event):
    find_button.config(image=find_btn_inactive_new)

def press():
    root.destroy()

Background_Label = Label(root, image=background_new_image_login)
Background_Label.pack(fill=BOTH)

quit_button = Button(Background_Label, image=quit_btn_new, bd=0, relief='sunken', bg='#D1E4FB', activebackground='#D1E4FB', command=press, highlightbackground='#D1E4FB')
quit_button.place(x=1460, y=-1)

find_button = Button(Background_Label, image=find_btn_inactive_new, bd=0, relief='sunken', bg='#17224E', activebackground='#17224E', highlightbackground='#17224E', command=make)
find_button.place(x=580, y=700)

find_button.bind('<Enter>', find_enter)
find_button.bind('<Leave>', find_exit)

ticker_ID_Entry_stock_predictor_input = Entry(root, font=Font2, relief="groove", highlightbackground="#0047AB", highlightcolor="#0047AB", highlightthickness=2, fg="#17224E", bg='#D1E4FB')
ticker_ID_Entry_stock_predictor_input.place(x=550, y=365)

parameter_stock_predictor_input = Entry(root, font=Font2, relief="groove", highlightbackground="#0047AB", highlightcolor="#0047AB", highlightthickness=2, fg="#17224E", bg='#D1E4FB')
parameter_stock_predictor_input.place(x=550, y=490)

root.mainloop()