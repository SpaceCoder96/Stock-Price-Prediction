from tkinter import *
from tkinter.font import Font
from subprocess import call
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
import os.path
import os
import time
import pickle

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

background_image_login = Image.open("assets\Background\login_bg.png")
background_resized_login = background_image_login.resize((1534, 860), Image.ANTIALIAS)
background_new_image_login = ImageTk.PhotoImage(background_resized_login)

Background_Label = Label(root, image=background_new_image_login, border=0, relief='sunken', bd=0)
Background_Label.pack(fill=BOTH)

login_btn_inactive = Image.open("assets\Buttons\login_btn_inactive.png")
login_btn_inactive_resized = login_btn_inactive.resize((350, 94), Image.ANTIALIAS)
login_btn_inactive_new = ImageTk.PhotoImage(login_btn_inactive_resized)

login_btn_active = Image.open("assets\Buttons\login_btn_active.png")
login_btn_active_resized = login_btn_active.resize((350, 94), Image.ANTIALIAS)
login_btn_active_new = ImageTk.PhotoImage(login_btn_active_resized)

create_btn_inactive = Image.open("assets\Buttons\create_btn_inactive.png")
create_btn_inactive_resized = create_btn_inactive.resize((450, 94), Image.ANTIALIAS)
create_btn_inactive_new = ImageTk.PhotoImage(create_btn_inactive_resized)

create_btn_active = Image.open("assets\Buttons\create_btn_active.png")
create_btn_active_resized = create_btn_active.resize((450, 94), Image.ANTIALIAS)
create_btn_active_new = ImageTk.PhotoImage(create_btn_active_resized)

quit_btn = Image.open("assets\Buttons\quit_btn_dark.png")
quit_btn_resized = quit_btn.resize((54, 89), Image.ANTIALIAS)
quit_btn_new = ImageTk.PhotoImage(quit_btn_resized)

def login():
    username = str(Username_Entry.get())
    password = str(Password_Entry.get())
    credentials_final = str(f'{username}|{password}')
    connection_credentials = sqlite3.connect(rf'assets\usr\Credentials.db')
    cursor_credentials = connection_credentials.cursor()
    cursor_credentials.execute('SELECT * FROM credentials')
    items = cursor_credentials.fetchall()
    for item in items:
        if credentials_final == item[3]:
            email = item[1]
            filepath = r"assets\usr\current.dat"
            exist = os.path.isfile(filepath)
            if exist == False:
                output = open(filepath, 'wb')
                pickle.dump(email, output)
                output.close()
                root.destroy()
                call(['python', 'Options.py'])
            else:
                os.remove(filepath)
                output = open(filepath, 'wb')
                pickle.dump(email, output)
                output.close()
                root.destroy()
                call(['python', 'Options.py'])
        else:
            messagebox.showerror("Error", "Credentials Do not Match")
            Username_Entry.delete(0, END)
            Password_Entry.delete(0, END)


def create():
    root.destroy()
    call(['python', 'Create Account.py'])

def login_enter(event):
    login_button.config(image=login_btn_active_new)

def login_exit(event):
    login_button.config(image=login_btn_inactive_new)

def create_enter(event):
    create_button.config(image=create_btn_active_new)

def create_exit(event):
    create_button.config(image=create_btn_inactive_new)

def press():
    root.destroy()

quit_button = Button(Background_Label, image=quit_btn_new, bd=0, relief='sunken', bg='#17224E', activebackground='#17224E', command=press, highlightbackground='#17224E')
quit_button.place(x=1460, y=0)

Username_Entry = Entry(Background_Label, bg='#D1E4FB', highlightcolor='#047FFF', fg='#17224E', font=Font2, highlightthickness=4, highlightbackground='#047FFF', width=30)
Username_Entry.place(x=800, y=245)

Password_Entry = Entry(Background_Label, bg='#D1E4FB', highlightcolor='#047FFF', fg='#17224E', font=Font2, highlightthickness=4, highlightbackground='#047FFF', width=30, show='•')
Password_Entry.place(x=800, y=400)

login_button = Button(Background_Label, image=login_btn_inactive_new, bd=0, relief='sunken', bg='#17224E', activebackground='#17224E', highlightbackground='#17224E', command=login)
login_button.place(x=950, y=550)

create_button = Button(Background_Label, image=create_btn_inactive_new, bd=0, relief='sunken', bg='#17224E', activebackground='#17224E', highlightbackground='#17224E', command=create)
create_button.place(x=900, y=750)

login_button.bind('<Enter>', login_enter)
login_button.bind('<Leave>', login_exit)

create_button.bind('<Enter>', create_enter)
create_button.bind('<Leave>', create_exit)


root.mainloop()