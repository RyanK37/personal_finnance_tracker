import random as rd
import tkinter as tk
import sqlite3 as sq

user_data=[{"User" : "Ryan", "Password": "1234"}, {"User" : "Hanna", "Password": "1234"}]

transistions_data = []

main_window = tk.Tk()
main_window.geometry("400x300")
main_window.title("Log-in Page")

username = tk.Label(main_window, text="Username", font=("calibri", 14))
username.grid(row = 1, column=0)

password = tk.Label(main_window, text="Password", font=("calibri", 14))
password.grid(row = 2, column=0)

user_entry = tk.Entry(main_window, font=("calibri", 14))
user_entry.grid(row=1, column=1)

pass_entry = tk.Entry(main_window, show="*", font=("calibri", 14))
pass_entry.grid(row=2, column=1)

def log_in():
    flag = False
    for data in user_data:
        if user_entry.get() == data["User"] and pass_entry.get() == data["Password"]:
            successful(data["User"])
            flag = True
            return
        
    if (flag == False):
        print("invalid user or password")
        
def successful(name):
    main_window.destroy()
    temp = tk.Tk()
    temp.geometry("400x300")
    greeting = tk.Label(temp, text="Welcome from personal finnace tracker " + name , font=("calibri", 14))
    greeting.pack(padx=0)
    temp.mainloop()
    
        
def register(user_data):
    new_user = user_entry.get()
    new_password = pass_entry.get()    
    new_user_data = [{"User" : new_user, "Password" : new_password}]
    user_data += new_user_data
    successful(new_user)

def clear():
    user_entry.delete(0, "end")
    pass_entry.delete(0, tk.END)


submit_icon = tk.Button(main_window, text="Submit", font=("calibri", 14), command=log_in)
submit_icon.grid(row =3, column=0)

register_icon = tk.Button(main_window, text="Register", font=("calibri", 14), command=lambda: register(user_data))
register_icon.grid(row = 4, column=0)

clear_btn = tk.Button(main_window, text="Clear", font=("calibri", 14), command=clear)
clear_btn.grid(row=3, column=1)


main_window.mainloop()