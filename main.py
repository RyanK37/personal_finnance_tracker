import random as rd
import tkinter as tk
import sqlite3 as sq

user_data=[{"User" : "Ryan", "Password": "1234"}, {"User" : "Hanna", "Password": "1234"}]

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

pass_entry = tk.Entry(main_window, show=" ", font=("calibri", 14))
pass_entry.grid(row=2, column=1)

def check_pass():
    flag = False
    for i in user_data:
        if user_entry.get() == i["User"] and pass_entry.get() == i["Password"]:
            print("Log in successful")
            print("welcome from personal finnace tracker " + i["User"] )
            flag = True
            return
    if (flag == False):
        print("invalid user or password")
        
def register(user_data):
    new_user = user_entry.get()
    new_password = pass_entry.get()    
    new_user_data = [{"User" : new_user, "Password" : new_password}]
    user_data += new_user_data
    print("successful register")

def print_test():
    print(user_data)
        
def clear():
    user_entry.delete(0, "end")
    pass_entry.delete(0, tk.END)


def change_window():
    main_window.destroy()  
    new_window = tk.Tk()
    new_window.title("Log-in Page")
    new_window.geometry("400x200")
    new_window.mainloop()


submit_icon = tk.Button(main_window, text="Submit", font=("calibri", 14), command=check_pass)
submit_icon.grid(row =3, column=0)

register_icon = tk.Button(main_window, text="Register", font=("calibri", 14), command=lambda: register(user_data))
register_icon.grid(row = 4, column=0)

clear_btn = tk.Button(main_window, text="Clear", font=("calibri", 14), command=clear)
clear_btn.grid(row=3, column=1)

test_btn = tk.Button(main_window, text="test", font = ("calibri", 14), command=print_test)
test_btn.grid(row=5, column=0)



main_window.mainloop()