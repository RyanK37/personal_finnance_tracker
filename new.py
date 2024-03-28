import tkinter as tk
import random as rd

account_balance = 0
tran_data = []

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

def update_balance_label():
    balance.config(text="Current balance : " + str(account_balance))

# ========================================================================

def show_tran():
    tran2 = tk.Tk()
    tran2.geometry("700x400")
    tran2.title("Dashboard")
    if len(tran_data) == 0 :
        empty_data = tk.Label(tran2, text="Empty transation", font=("calibri", 14))
        empty_data.pack()
        
    for data in tran_data:
        show = tk.Label(tran2, text=str(data), font=("calibri", 14))
        show.pack()
    tran2.mainloop()
        
# ========================================================================

def update_tran_data(type, category, amount, date, source):
    global account_balance, tran_data
    check_unique = set()
    new = rd.randint(1000, 9999)
    if new not in check_unique:
        random_id = new
        check_unique.add(new)
            
    new_tran_data = {"ID" : random_id, "type" : type , "category" : category, "amount" : amount, "payee/source" : source, "date" : date}
    tran_data.append(new_tran_data)
    
    if type == "Income":
        account_balance += amount
        
    elif type == "Expenses":
        account_balance -= amount
    update_balance_label()
    add_window.destroy()

# =====================================================================

def add_tran():
    global add_window
    add_window =tk.Tk()
    add_window.geometry("500x500")
    add_window.title("Add Transations")
    
    radio_frame = tk.Frame(add_window)
    radio_frame.pack()
    
    choose_type = tk.StringVar(value="Income")
    income_radio = tk.Radiobutton(radio_frame, text="Income", variable=choose_type, value="Income")
    income_radio.pack(side="left")
    expense_radio = tk.Radiobutton(radio_frame, text="Expenses", variable=choose_type, value="Expenses")
    expense_radio.pack(side="right")
    
    categories = {"Income": ["Salary", "Pension", "Interest", "Others"],
                  "Expenses": ["Food", "Rent", "Clothing", "Car", "Health", "Others"]}
    category_real = tk.StringVar(value="Salary")
    
    category_label =tk.Label(add_window, text="Category")
    category_label.pack()
    category_menu = tk.OptionMenu(add_window, category_real, *categories["Income"] + categories["Expenses"])
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
    
    add_btn = tk.Button(add_window, text="Submit" , font=("calibri", 14), command=lambda : update_tran_data(choose_type.get(), category_real.get(), int(amount_entry.get()), date_entry.get(), source_entry.get()))
    add_btn.pack()
    add_window.mainloop()
    
# ======================================================================================================

def del_tran():
    del_window = tk.Tk()
    del_window.geometry("300x300")
    del_window.title("Delete transations")
    
    id_label = tk.Label(del_window, text="Please input ID to delete!")
    id_label.pack()
    id_entry = tk.Entry(del_window)
    id_entry.pack()
    
    global tran_data
    def delete_update():
        global account_balance
        for i in tran_data:
            if i["ID"] == int(id_entry.get()):
                if i["type"] == "Income":
                    account_balance -= i["amount"]
                elif i["type"] == "Expenses":
                    account_balance += i["amount"]
                    tran_data.remove(i)
                update_balance_label()
        del_window.destroy()
    
    del_btn = tk.Button(del_window, text="Delete", font=("calibri", 14), command=delete_update)
    del_btn.pack()
    del_window.mainloop()

# ======================================================================================================

def tran_1():
    tran1 = tk.Tk()
    tran1.geometry("400x400")
    tran1.title("Personal Finnace Tracker")
    
    welcome = tk.Label(tran1, text="Welcome " + str(username_entry.get()) , font=("calibri", 14))
    welcome.pack()
    
    start_window.destroy()
    
    global balance
    balance = tk.Label(tran1, text="Current balance : "  + str(account_balance), font=("calibri", 14))
    balance.pack()
    show_trans_btn = tk.Button(tran1, text="Summary", font=("calibri", 14), command=show_tran)
    show_trans_btn.pack()
    
    add_tran_btn = tk.Button(tran1, text="Add transation", font=("calibri", 14), command=add_tran)
    add_tran_btn.pack()
    
    del_tran_btn = tk.Button(tran1, text="Delete transation", font=("calibri" , 14), command=del_tran)
    del_tran_btn.pack()
    
    tran1.mainloop()
        
# ========================================================================
def clear():
    username_entry.delete(0, "end")
    password_entry.delete(0, tk.END)


submit_icon = tk.Button(start_window, text="Submit", font=("calibri", 14), command=tran_1)
submit_icon.grid(row =4, column=0)

clear_btn = tk.Button(start_window, text="Clear", font=("calibri", 14), command=clear)
clear_btn.grid(row=4, column=1)

start_window.mainloop()
