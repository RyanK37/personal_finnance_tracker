import random as r
import tkinter as tk
import sqlite3 as sq

connect = sq.connect("python_final.db")
cur = connect.cursor()
print("Welcome to the Personal Finance Tracker")

cur.execute("drop table if exists Users_data")
cur.execute("create table Users_data(ID integer primary key, Username text, Password text) ")

main_window = tk.Tk()
main_window.geometry("400x300")
main_window.title("Log-in Page")

greeting = tk.Label(main_window, text="Welcome to our website", font=("calibri", 14))
greeting.grid(row = 0, column=0)

username = tk.Label(main_window, text="Username", font=("calibri", 14))
username.grid(row = 1, column=0)

password = tk.Label(main_window, text="Password", font=("calibri", 14))
password.grid(row = 2, column=0)

user_entry = tk.Entry(main_window, font=("calibri", 14))
user_entry.grid(row=1, column=1)

pass_entry = tk.Entry(main_window, show="*", font=("calibri", 14))
pass_entry.grid(row=2, column=1)

def check_pass():
    if (user_entry.get() == "Ryan") & (pass_entry.get() == "123456"):
        print("Log in successful")
    else:
        print("INvalid username or password")
        
def clear():
    user_entry.delete(0, "end")
    pass_entry.delete(0, tk.END)
    
submit_icon = tk.Button(main_window, text="Submit", font=("calibri", 14), command=check_pass)
submit_icon.grid(row =3, column=0)

clear_btn = tk.Button(main_window, text="Clear", font=("calibri", 14), command=clear)
clear_btn.grid(row=3, column=1)




cur.close()
connect.close()

main_window.mainloop()