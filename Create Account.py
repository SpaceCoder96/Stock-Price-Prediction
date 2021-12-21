from tkinter import *
from tkinter.font import Font
from subprocess import call
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
import os.path
import os
import sqlite3

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

create_btn_inactive = Image.open("assets\Buttons\create_btn_inactive.png")
create_btn_inactive_resized = create_btn_inactive.resize((450, 94), Image.ANTIALIAS)
create_btn_inactive_new = ImageTk.PhotoImage(create_btn_inactive_resized)

create_btn_active = Image.open("assets\Buttons\create_btn_active.png")
create_btn_active_resized = create_btn_active.resize((450, 94), Image.ANTIALIAS)
create_btn_active_new = ImageTk.PhotoImage(create_btn_active_resized)

background_image_login = Image.open("assets\Background\create_new_account_bg.png")
background_resized_login = background_image_login.resize((1534, 860), Image.ANTIALIAS)
background_new_image_login = ImageTk.PhotoImage(background_resized_login)

quit_btn = Image.open("assets\Buttons\quit_btn_light.png")
quit_btn_resized = quit_btn.resize((54, 89), Image.ANTIALIAS)
quit_btn_new = ImageTk.PhotoImage(quit_btn_resized)

def create_enter(event):
    create_button.config(image=create_btn_active_new)

def create_exit(event):
    create_button.config(image=create_btn_inactive_new)

def press():
    root.destroy()

def create():
    username = str(Username_Entry.get())
    email = str(Email_Entry.get())
    password = str(Password_Entry.get())
    cpassword = str(CPassword_Entry.get())
    credentials_final = str(f'{username}|{password}')

    if len(username) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning("Warning", "Please fill all fields")
        Username_Entry.delete(0, END)
        Password_Entry.delete(0, END)
        CPassword_Entry.delete(0, END)
        Email_Entry.delete(0, END)

    else:
        if password == cpassword:
            dir_path = rf'assets\usr\{email}'
            dir_exist = os.path.isdir(dir_path)
            if dir_exist == False:
                os.mkdir(dir_path)
            else:
                pass
            cred_exist = os.path.isfile(rf'assets\usr\Credentials.db')
            if cred_exist == False:
                connection_credentials = sqlite3.connect(rf'assets\usr\Credentials.db')
                cursor_credentials = connection_credentials.cursor()
                connection_credentials.commit()
                cursor_credentials.execute("""CREATE TABLE credentials (
                    credentials text,
                    email text,
                    password text, 
                    cred_final text
                )""")
                connection_credentials.commit()
            else:
                connection_credentials = sqlite3.connect(rf'assets\usr\Credentials.db')
                cursor_credentials = connection_credentials.cursor()
                connection_credentials.commit()
            cursor_credentials.execute(f"INSERT INTO credentials VALUES ('{username}', '{email}', '{password}', '{credentials_final}')")
            connection_credentials.commit()
            connection_credentials.close()

            root.destroy()
            call(['python', 'Login.py'])

        else:
            messagebox.showerror("Error", "Password Does not Match")
            Username_Entry.delete(0, END)
            Password_Entry.delete(0, END)
            CPassword_Entry.delete(0, END)
            Email_Entry.delete(0, END)

Background_Label = Label(root, image=background_new_image_login)
Background_Label.pack(fill=BOTH)

Username_Entry = Entry(Background_Label, bg='#D1E4FB', highlightcolor='#047FFF', fg='#17224E', font=Font2, highlightthickness=4, highlightbackground='#047FFF', width=30)
Username_Entry.place(x=100, y=250)

Email_Entry = Entry(Background_Label, bg='#D1E4FB', highlightcolor='#047FFF', fg='#17224E', font=Font2, highlightthickness=4, highlightbackground='#047FFF', width=30)
Email_Entry.place(x=100, y=375)

Password_Entry = Entry(Background_Label, bg='#D1E4FB', highlightcolor='#047FFF', fg='#17224E', font=Font2, highlightthickness=4, highlightbackground='#047FFF', width=30, show='•')
Password_Entry.place(x=100, y=500)

CPassword_Entry = Entry(Background_Label, bg='#D1E4FB', highlightcolor='#047FFF', fg='#17224E', font=Font2, highlightthickness=4, highlightbackground='#047FFF', width=30, show='•')
CPassword_Entry.place(x=100, y=625)

create_button = Button(Background_Label, image=create_btn_inactive_new, bd=0, relief='sunken', bg='#17224E', activebackground='#17224E', highlightbackground='#17224E', command=create)
create_button.place(x=175, y=750)

quit_button = Button(Background_Label, image=quit_btn_new, bd=0, relief='sunken', bg='#D1E4FB', activebackground='#D1E4FB', command=press, highlightbackground='#D1E4FB')
quit_button.place(x=1460, y=-1)

create_button.bind('<Enter>', create_enter)
create_button.bind('<Leave>', create_exit)

root.mainloop()