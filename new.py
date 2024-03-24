import tkinter as tk
import random as rd

account_balance = 0
tran_data = [{"ID" : 12345, "type" : "Income", "category" : "Salary", "amount" : 1000, "payee/source" : "salary","date" : "2-April"  }]

# ========================================================================

start_window = tk.Tk()
start_window.geometry("400x300")
start_window.title("Personal Finnace Tracker")

username = tk.Label(start_window, text="Username", font=("calibri", 14))
username.grid(row = 1, column=0)

password = tk.Label(start_window, text="Password", font=("calibri", 14))
password.grid(row = 2, column=0)

username_entry = tk.Entry(start_window, font=("calibri", 14))
username_entry.grid(row=1, column=1)

password_entry = tk.Entry(start_window, show="*", font=("calibri", 14))
password_entry.grid(row=2, column=1)

# ========================================================================

def show_tran(window):
    window.withdraw()
    tran2 = tk.Tk()
    tran2.geometry("700x400")
    
    for data in tran_data:
        show = tk.Label(tran2, text=f"ID : {data['ID']} | Type : {data['type']} | Category : {data['category']} | Amount : {data['amount']} | payee/source : {data['payee/source']} |date : {data['date']}", font=("calibri", 14))
        show.pack()
    tran2.mainloop()
        

# ========================================================================
def add_tran():
    add_window =tk.Tk()
    add_window.geometry("500x500")
    
    radio_frame = tk.Frame()
    radio_frame.pack()
    choose_type = tk.StringVar(value="Income")
    income_radio = tk.Radiobutton(radio_frame, text="Income", variable=choose_type, value="Income")
    income_radio.pack(side="left")
    expense_radio = tk.Radiobutton(radio_frame, text="Expenses", variable=choose_type, value="Expenses")
    expense_radio.pack(side="right")
    
    categories = {"Income": ["Salary", "Pension", "Interest", "Others"],
                  "Expenses": ["Food", "Rent", "Clothing", "Car", "Health", "Others"]}
    category_start = tk.StringVar(value="Salary")
    
    # def update_type():
    #     if choose_type.get() == "Income":
    #         category_start.set(categories["Income"][0])
    #         category_menu.config(*categories["Income"])
    #     elif choose_type.get() == "Expenses":
    #         category_start.set(categories["Expenses"][0])
    #         category_menu.config(*categories["Expenses"])
    
    # choose_type.trace_add("write", update_type)
    
    category_label =tk.Label(add_window, text="Category")
    category_label.pack()
    category_menu = tk.OptionMenu(add_window, category_start, *categories["Income"] + categories["Expenses"])
    category_menu.pack()
    
    amount_label = tk.Label(add_window, text="Amount")
    amount_label.pack()
    amount_entry = tk.Entry(add_window)
    amount_entry.pack()
    
    date_label = tk.Label(add_window, text="Date")
    date_label.pack()
    date_entry = tk.Entry(add_window)
    date_entry.pack()
    
    source_label = tk.Label(add_window, text="Payee/Source")
    source_label.pack()
    source_entry = tk.Entry(add_window)
    source_entry.pack()
    
    add_btn = tk.Button(add_window, text="Submit" , font=("calibri", 14))
    add_btn.pack()
    add_window.mainloop()
    
# ======================================================================================================
def tran_1():
    tran1 = tk.Tk()
    tran1.geometry("400x400")
    tran1.title("Personal Finnace Tracker")
    
    welcome = tk.Label(tran1, text="Welcome " + str(username_entry.get()) , font=("calibri", 14))
    welcome.pack()
    
    start_window.destroy()
    
    balance = tk.Label(tran1, text="Current balance : "  + str(account_balance), font=("calibri", 14))
    balance.pack()
    show_trans_btn = tk.Button(tran1, text="Show Transistions", font=("calibri", 14), command= lambda: show_tran(tran1))
    show_trans_btn.pack()
    
    test = tk.Button(tran1, text="test", command=add_tran)
    test.pack()
        
    tran1.mainloop()
# ========================================================================
def clear():
    username_entry.delete(0, "end")
    password_entry.delete(0, tk.END)


submit_icon = tk.Button(start_window, text="Submit", font=("calibri", 14), command=tran_1)
submit_icon.grid(row =3, column=0)

clear_btn = tk.Button(start_window, text="Clear", font=("calibri", 14), command=clear)
clear_btn.grid(row=3, column=1)

start_window.mainloop()