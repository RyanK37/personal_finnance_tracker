import tkinter as tk
import random as rd
import matplotlib.pyplot as plt
import pandas as pd

account_balance = 0
tran_data = []
user = ""

# ===============================================================================================================================

start_window = tk.Tk()                                                                      #Strat window to take useranme and password
start_window.geometry("350x200")
start_window.title("Personal Finnace Tracker")

username = tk.Label(start_window, text="Username", font=("calibri", 14))
username.grid(row = 1, column=0)

password = tk.Label(start_window, text="Password", font=("calibri", 14))
password.grid(row = 2, column=0)

username_entry = tk.Entry(start_window, font=("calibri", 14))
username_entry.grid(row=1, column=1)

password_entry = tk.Entry(start_window, show="*", font=("calibri", 14))
password_entry.grid(row=2, column=1)

def clear():
    username_entry.delete(0, "end")
    password_entry.delete(0, tk.END)

# ===============================================================================================================================

def update_balance_label():
    balance.config(text="Current balance : " + str(account_balance))
    
# ===============================================================================================================================

def update_last_tran():
    if tran_data == []:
        last_tran_label.config(text="No transation currently!!")
    else:
        last_tran_label.config(text="Last Transation : " + str(tran_data[-1]))

# ===============================================================================================================================      

def destroy_window(window):
    window.destroy()

# ===============================================================================================================================

def empty_transation_window():
    temp = tk.Tk()
    temp.title("Empty Transation")
    temp.geometry("400x100")
    empty_label = tk.Label(temp, text="There is no transation", font=("calibri", 14))
    empty_label.pack()
    temp.after(1500, lambda:destroy_window(temp))
    temp.mainloop()

# ===============================================================================================================================

def go_back(current, previous):
    current.destroy()
    previous.deiconify()
    
# ===============================================================================================================================

def update_tran_data(type, category, amount, date, source):
    global account_balance, tran_data
    check_unique = set()
    new = rd.randint(1000, 9999)
    if new not in check_unique:
        random_id = new
        check_unique.add(new)
            
    new_tran_data = {"ID" : random_id, "Type" : type , "Category" : category, "Amount" : amount, "Payee/Source" : source, "Date" : date}
    tran_data.append(new_tran_data)
    
    if type == "Income":
        account_balance += amount
    elif type == "Expense":
        account_balance -= amount
        
    update_balance_label()
    update_last_tran()  
    add_window.destroy()

# ===============================================================================================================================

def filter_by_input(start, end, type, category, source):
        start_date = pd.to_datetime(start, format="%d-%b-%Y")
        end_date = pd.to_datetime(end, format="%d-%b-%Y")
        
        filtered_list = []
        for each_data in tran_data:
            if start_date <= pd.to_datetime(each_data["Date"], format="%d-%b-%Y") <= end_date and\
                each_data["Type"] == type and\
                each_data["Category"] == category and\
                each_data["Payee/Source"].lower() == source.lower():
                filtered_list.append(each_data)
        return filtered_list
    
# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------

def filter_by_time(start, end, type):
    start_date = pd.to_datetime(start, format="%d-%b-%Y")
    end_date = pd.to_datetime(end, format="%d-%b-%Y")
        
    filtered_list = []
    for each_data in tran_data:
        if start_date <= pd.to_datetime(each_data["Date"], format="%d-%b-%Y") <= end_date and each_data["Type"] == type:
            filtered_list.append(each_data)
    return filtered_list

# ===============================================================================================================================

def draw_piechart(data_list, pie_data):
    total_amount  = {}
    types = data_list[0]["Type"]
    for each in data_list:
        category = each["Category"]
        amount = each["Amount"]
        if category in total_amount:
            total_amount[category] += amount
        else:
            total_amount[category] = amount
    
    label = total_amount.keys()
    size = total_amount.values()
    
    pie_data.pie(size, labels=label, autopct='%1.1f%%')
    pie_data.set_title(types)
    pie_data.legend(bbox_to_anchor =(0.5,-0.1), loc="lower center")

# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------

def draw_barchart(data_list, bar_data):
    total_amount  = {}
    types = data_list[0]["Type"]
    for each in data_list:
        category = each["Category"]
        amount = each["Amount"]
        if category in total_amount:
            total_amount[category] += amount
        else:
            total_amount[category] = amount
    
    label = list(total_amount.keys())
    size = list(total_amount.values())
    
    bar_data.bar(label, size)
    bar_data.set_title(types)
    bar_data.set_xlabel("Category")
    bar_data.set_ylabel("Amount")

# ===============================================================================================================================

def write_file(data_list, filename):
    if data_list == []:
        empty_transation_window()
    else:
        keys = list(data_list[0].keys())                            
        key_widths = {}
        for each in keys:
            key_widths[each] = len(each)

        column_widths = {}
        for data in data_list:
            for key in keys:
                if data[key] is None:
                    data[key] = ""
                column_widths[key] = max(key_widths[key], len(str(data[key]))) 
        # ---------------------------------------------------------------------------------        
        with open(filename, 'w') as file:
            file.write("Personal Finnace Tracker\n")
            file.write("User Name : " + str(user) + "\n")
            file.write("\n")
            
            total_place = 0
            for key in keys:
                left_place = column_widths[key] - len(key)
                file.write(key + (" " * left_place) + " | " )
                total_place += (column_widths[key] + 3 )
            file.write("\n")
            file.write("-"*total_place + "\n")
            
            for data in data_list:
                for key in keys:
                    values = str(data[key])
                    left_place = column_widths[key] - len(values)
                    file.write(values + (" " * left_place) + " | ")
                file.write("\n")
        # ---------------------------------------------------------------------------------
        temp = tk.Tk()
        temp.title("Print successful")
        temp.geometry("500x300")
        success_label = tk.Label(temp, text="The filtered transations are printed successfully!!", font=("calibri", 14))
        success_label.pack()
        temp.after(1000, destroy_window, temp)
        temp.mainloop()   

# ===============================================================================================================================

def show_all_trans(window):
    window.withdraw()

    all_trans_window = tk.Tk()
    all_trans_window.title("All Transations")
    all_trans_window.geometry("1200x350")    
    for each in tran_data:
        each_label = tk.Label(all_trans_window, text=str(each), font=("calibri", 14))
        each_label.pack()
    
    # ---------------------------------------------------------------------------------
    
    def determine_pie():
        income_list = [data for data in tran_data if data["Type"] == "Income" ]
        expense_list = [data for data in tran_data if data["Type"] == "Expense"]
        
        if income_list and expense_list:
            figure, pie_data = plt.subplots(1,2)
            draw_piechart(income_list, pie_data[0])
            draw_piechart(expense_list, pie_data[1])
            plt.show()
        elif income_list:
            figure, pie_data = plt.subplots()
            draw_piechart(income_list, pie_data)
            plt.show()
        elif expense_list:
            figure, pie_data = plt.subplots()
            draw_piechart(expense_list, pie_data)
            plt.show()
        else:
            empty_transation_window()
    
    # ---------------------------------------------------------------------------------
    
    def determine_barchart():
        income_list = [data for data in tran_data if data["Type"] == "Income" ]
        expense_list = [data for data in tran_data if data["Type"] == "Expense"]
        
        if income_list and expense_list:
            figure, bar_data = plt.subplots(2, 1)
            draw_barchart(income_list, bar_data[0])
            draw_barchart(expense_list, bar_data[1])
            plt.tight_layout()
            plt.show()
        elif income_list:
            figure, bar_data = plt.subplots()
            draw_barchart(income_list, bar_data)
            plt.show()
        elif expense_list:
            figure, bar_data = plt.subplots()
            draw_barchart(expense_list, bar_data)
            plt.show()
        else:
            empty_transation_window()
    
    # ---------------------------------------------------------------------------------
    
    print_all_tran = tk.Button(all_trans_window, text="Print All Transations", font=("calibri", 14), command=lambda: write_file(tran_data, "ALl_Transations.txt"))
    print_all_tran.pack()
    
    pie_chart_btn = tk.Button(all_trans_window, text="Pie Charts", font=("calibri", 14), command=determine_pie)
    pie_chart_btn.pack()
    
    # ---------------------------------------------------------------------------------
    temp_frame = tk.Frame(all_trans_window)
    temp_frame.pack()
    
    bar_chart_btn = tk.Button(temp_frame, text="Bar Charts", font=("calibri", 14), command=determine_barchart)
    bar_chart_btn.pack(side="left", padx=5, pady=5)
    
    go_back_btn =  tk.Button(temp_frame, text="Back", font=("calibri", 14), command=lambda: go_back(all_trans_window, window))
    go_back_btn.pack(side="right", padx=5, pady=5)
    # ---------------------------------------------------------------------------------
    
    all_trans_window.mainloop()
    
# ===============================================================================================================================
    
def piechart(previous_window):
    previous_window.withdraw()
    
    piechart_window = tk.Tk()
    piechart_window.geometry("500x400")
    piechart_window.title("Pie Chart")    
    
    # ---------------------------------------------------------------------------------    
    
    date_frame = tk.Frame(piechart_window)
    date_frame.pack()
    
    date_range_from_label = tk.Label(date_frame, text="Time Range(From)", font=("calibri", 14))
    date_range_from_label.grid(row=1, column=0)
    date_range_from = tk.Entry(date_frame)
    date_range_from.grid(row=1, column=1)
    
    date_range_to_label = tk.Label(date_frame, text="Time Range(To)", font=("calibri", 14))
    date_range_to_label.grid(row=2, column=0)
    date_range_to = tk.Entry(date_frame)
    date_range_to.grid(row=2, column=1)
    
    # ---------------------------------------------------------------------------------    
    
    radio_frame = tk.Frame(piechart_window)
    radio_frame.pack()
    
    choose_type = tk.StringVar(value="Income")
    income_radio = tk.Radiobutton(radio_frame, text="Income", variable=choose_type, value="Income", font=("calibri", 14))
    income_radio.pack(side="left")
    expense_radio = tk.Radiobutton(radio_frame, text="Expense", variable=choose_type, value="Expense", font=("calibri", 14))
    expense_radio.pack(side="right")
    
    # ---------------------------------------------------------------------------------    
    
    def draw_chart():
        filtered_data = filter_by_time(date_range_from.get(), date_range_to.get(), choose_type.get())
        if filtered_data == []:
            temp_window = tk.Tk()
            temp_window.geometry("600x200")
            temp_window.title("Empty transation!")
            empty_alert = tk.Label(temp_window, text="There is no transation within the filtered range!!", font=("calibri", 16))
            empty_alert.pack()
            temp_window.mainloop()
        else:
            figure, pie_data = plt.subplots()
            draw_piechart(filtered_data, pie_data)
            plt.show()
    
    # ---------------------------------------------------------------------------------    
        
    draw_piechart_btn = tk.Button(piechart_window, text="Draw Pie Chart", font=("calibri", 14), command=draw_chart)
    draw_piechart_btn.pack()
    
    go_back_btn =  tk.Button(piechart_window, text="Back", font=("calibri", 14), command=lambda: go_back(piechart_window, previous_window))
    go_back_btn.pack()
    
    piechart_window.mainloop()
    
# ===============================================================================================================================

def barchart(previous_window):
    previous_window.withdraw()
    
    barchart_window = tk.Tk()
    barchart_window.geometry("500x400")
    barchart_window.title("Pie Chart")     
        
    # ---------------------------------------------------------------------------------    
    
    date_frame = tk.Frame(barchart_window)
    date_frame.pack()
    
    date_range_from_label = tk.Label(date_frame, text="Time Range(From)", font=("calibri", 14))
    date_range_from_label.grid(row=1, column=0)
    date_range_from = tk.Entry(date_frame)
    date_range_from.grid(row=1, column=1)
    
    date_range_to_label = tk.Label(date_frame, text="Time Range(To)", font=("calibri", 14))
    date_range_to_label.grid(row=2, column=0)
    date_range_to = tk.Entry(date_frame)
    date_range_to.grid(row=2, column=1)
            
    # ---------------------------------------------------------------------------------    
   
    radio_frame = tk.Frame(barchart_window)
    radio_frame.pack()
    
    choose_type = tk.StringVar(value="Income")
    income_radio = tk.Radiobutton(radio_frame, text="Income", variable=choose_type, value="Income", font=("calibri", 14))
    income_radio.pack(side="left")
    expense_radio = tk.Radiobutton(radio_frame, text="Expense", variable=choose_type, value="Expense", font=("calibri", 14))
    expense_radio.pack(side="right")
                
    # ---------------------------------------------------------------------------------    
    
    def draw_chart():
        filtered_data = filter_by_time(date_range_from.get(), date_range_to.get(), choose_type.get())
        if filtered_data == []:
            temp_window = tk.Tk()
            temp_window.geometry("600x200")
            temp_window.title("Empty transation!")
            empty_alert = tk.Label(temp_window, text="There is no transation within the filtered range!!", font=("calibri", 16))
            empty_alert.pack()
            temp_window.mainloop()
        else:
            figure, bar_data = plt.subplots()
            draw_barchart(filtered_data, bar_data)
            plt.show()
                        
    # ---------------------------------------------------------------------------------    
        
    draw_barchart_btn = tk.Button(barchart_window, text="Draw Bar Chart", font=("calibri", 14), command=draw_chart)
    draw_barchart_btn.pack()
    
    go_back_btn =  tk.Button(barchart_window, text="Back", font=("calibri", 14), command=lambda: go_back(barchart_window, previous_window))
    go_back_btn.pack()
    
    barchart_window.mainloop()
    
# ===============================================================================================================================

def summary():
    summary_window = tk.Tk()
    summary_window.geometry("700x400")
    summary_window.title("Dashboard")
                
    # ---------------------------------------------------------------------------------    
    
    date_frame = tk.Frame(summary_window)
    date_frame.pack()
    
    date_range_from_label = tk.Label(date_frame, text="Time Range(From)", font=("calibri", 14))
    date_range_from_label.grid(row=1, column=0)
    date_range_from = tk.Entry(date_frame)
    date_range_from.grid(row=1, column=1)
    
    date_range_to_label = tk.Label(date_frame, text="Time Range(To)", font=("calibri", 14))
    date_range_to_label.grid(row=2, column=0)
    date_range_to = tk.Entry(date_frame)
    date_range_to.grid(row=2, column=1)
                
    # ---------------------------------------------------------------------------------    
    
    radio_frame = tk.Frame(summary_window)
    radio_frame.pack()
    
    choose_type = tk.StringVar(value="Income")
    income_radio = tk.Radiobutton(radio_frame, text="Income", variable=choose_type, value="Income", font=("calibri", 14))
    income_radio.pack(side="left")
    expense_radio = tk.Radiobutton(radio_frame, text="Expense", variable=choose_type, value="Expense", font=("calibri", 14))
    expense_radio.pack(side="right")
                
    # ---------------------------------------------------------------------------------    
    
    option_frame = tk.Frame(summary_window)
    option_frame.pack()
    categories = {"Income": ["Salary", "Pension", "Interest", "Others"],
                  "Expense": ["Food", "Rent", "Clothing", "Car", "Health", "Others"]}
    category_real = tk.StringVar(value="Salary")
    
    category_label =tk.Label(option_frame, text="Category: ",  font=("calibri", 14))
    category_label.pack(side="left")
    category_menu = tk.OptionMenu(option_frame, category_real, *(categories["Income"] + categories["Expense"]))
    category_menu.pack(side="right")
    
                
    # ---------------------------------------------------------------------------------    
    
    source_label = tk.Label(summary_window, text="Payee/Source",  font=("calibri", 14))
    source_label.pack()
    source_entry = tk.Entry(summary_window)
    source_entry.pack()
    
    # ---------------------------------------------------------------------------------
    
    def show_filtered_data():
        filtered_data = filter_by_input(date_range_from.get(), date_range_to.get(), choose_type.get(), category_real.get(), source_entry.get())
        summary_window.withdraw()
        temp_window = tk.Tk()
        temp_window.title("Filterd transations")
        temp_window.geometry("800x500")
        
        if filtered_data == []:
            filtered_label = tk.Label(temp_window, text="There is no transation!!", font=("calibri", 14))
            filtered_label.pack()
        else:
            for each in filtered_data:
                filtered_label = tk.Label(temp_window, text=str(each), font=("calibri", 14))
                filtered_label.pack()
        temp_frame = tk.Frame(temp_window)
        temp_frame.pack()
        print_btn = tk.Button(temp_frame, text="Print", font=("calibri", 14), command=lambda: write_file(filtered_data, "Filtered_Transations.txt"))
        print_btn.pack(side="left", padx=5, pady=5)
        
        go_back_btn =  tk.Button(temp_frame, text="Back", font=("calibri", 14), command=lambda: go_back(temp_window, summary_window))
        go_back_btn.pack(side="right", padx=5, pady=5)
        
        temp_window.mainloop()
            
    # ---------------------------------------------------------------------------------
    
    btn_frame = tk.Frame()
    btn_frame.pack(padx=5, pady=5)
    show_btn = tk.Button(btn_frame, text="Show Filtered Transations", font=("calibri", 14), command=show_filtered_data)
    show_btn.pack(side="left", padx=5, pady=5)
    
    all_tran_btn = tk.Button(btn_frame, text="All Transations", font=("calibri", 14), command=lambda: show_all_trans(summary_window))
    all_tran_btn.pack(side="right", padx=5, pady=5)
                
    # ---------------------------------------------------------------------------------    
    
    barchart_btn = tk.Button(summary_window, text="Bar Chart", font=("calibri", 14), command=lambda: barchart(summary_window))
    barchart_btn.pack(padx=5, pady=5)
    
    piechart_btn = tk.Button(summary_window, text="Pie Chart",  font=("calibri", 14), command=lambda: piechart(summary_window))
    piechart_btn.pack(padx=5, pady=5)
                
    # ---------------------------------------------------------------------------------    
    
    summary_window.mainloop()
        
# ===============================================================================================================================

def add_tran():
    global add_window
    add_window =tk.Tk()
    add_window.geometry("500x500")
    add_window.title("Add Transations")
    
    # ---------------------------------------------------------------------------------
    
    radio_frame = tk.Frame(add_window)
    radio_frame.pack()
    
    choose_type = tk.StringVar(value="Income")
    income_radio = tk.Radiobutton(radio_frame, text="Income", variable=choose_type, value="Income", font=("calibri", 14))
    income_radio.pack(side="left")
    expense_radio = tk.Radiobutton(radio_frame, text="Expense", variable=choose_type, value="Expense", font=("calibri", 14))
    expense_radio.pack(side="right")
    
    # ---------------------------------------------------------------------------------
    category_frame = tk.Frame(add_window)
    category_frame.pack()
    categories = {"Income": ["Salary", "Pension", "Interest", "Others"],
                  "Expense": ["Food", "Rent", "Clothing", "Car", "Health", "Others"]}
    category_real = tk.StringVar(value="Salary")
    
    category_label =tk.Label(category_frame, text="Category:",  font=("calibri", 14))
    category_label.pack(side="left")
    category_menu = tk.OptionMenu(category_frame, category_real, *categories["Income"] + categories["Expense"])
    category_menu.pack(side="right")
       
    # ---------------------------------------------------------------------------------
     
    amount_label = tk.Label(add_window, text="Amount", font=("calibri", 14))
    amount_label.pack()
    amount_entry = tk.Entry(add_window)
    amount_entry.pack()
    
    date_label = tk.Label(add_window, text="Date(01-Apr-2004)",  font=("calibri", 14))
    date_label.pack()
    date_entry = tk.Entry(add_window)
    date_entry.pack()
    
    source_label = tk.Label(add_window, text="Payee/Source",  font=("calibri", 14))
    source_label.pack()
    source_entry = tk.Entry(add_window)
    source_entry.pack()
        
    # ---------------------------------------------------------------------------------
    
    add_btn = tk.Button(add_window, text="Submit" , font=("calibri", 14), command=lambda : update_tran_data(choose_type.get(), category_real.get(), int(amount_entry.get()), date_entry.get(), source_entry.get()))
    add_btn.pack()
        
    # ---------------------------------------------------------------------------------
    
    add_window.mainloop()
    
# ===============================================================================================================================

def del_tran():
    del_window = tk.Tk()
    del_window.geometry("300x300")
    del_window.title("Delete transations")
                
    # ---------------------------------------------------------------------------------    
    
    id_label = tk.Label(del_window, text="Please input ID to delete!")
    id_label.pack()
    id_entry = tk.Entry(del_window)
    id_entry.pack()
                
    # ---------------------------------------------------------------------------------    
    
    def delete_update():
        global account_balance
        for index, data in enumerate(tran_data):
            if data["ID"] == int(id_entry.get()):
                if data["Type"] == "Income":
                    account_balance -= data["Amount"]
                elif data["Type"] == "Expense":
                    account_balance += data["Amount"]
                
        del tran_data[index]
        update_balance_label()
        update_last_tran()
        del_window.destroy()
                
    # ---------------------------------------------------------------------------------    
    
    del_btn = tk.Button(del_window, text="Delete", font=("calibri", 14), command=delete_update)
    del_btn.pack()
    del_window.mainloop()

# ===============================================================================================================================

def main_window():
    main_window = tk.Tk()
    main_window.geometry("1200x400")
    main_window.title("Personal Finnace Tracker")
                
    # ---------------------------------------------------------------------------------    
    global user
    user = str(username_entry.get())
    welcome = tk.Label(main_window, text="Welcome " + str(username_entry.get()) + "!" , font=("calibri", 14))
    welcome.pack()
    
    start_window.destroy()
                
    # ---------------------------------------------------------------------------------    
    global balance
    balance = tk.Label(main_window, text="Current balance : "  + str(account_balance), font=("calibri", 14))
    balance.pack()

    global last_tran_label
    last_tran_label = tk.Label(main_window, text="No transation currently!!!", font=("calibri", 14))
    last_tran_label.pack()
                
    # ---------------------------------------------------------------------------------    
    summarys_btn = tk.Button(main_window, text="Summary", font=("calibri", 14), command=summary)
    summarys_btn.pack()
    
    add_tran_btn = tk.Button(main_window, text="Add transation", font=("calibri", 14), command=add_tran)
    add_tran_btn.pack()
    
    del_tran_btn = tk.Button(main_window, text="Delete transation", font=("calibri" , 14), command=del_tran)
    del_tran_btn.pack()
                
    # ---------------------------------------------------------------------------------    
    main_window.mainloop()
        
# ===============================================================================================================================

submit_icon = tk.Button(start_window, text="Submit", font=("calibri", 14), command=main_window)
submit_icon.grid(row =4, column=0)

clear_btn = tk.Button(start_window, text="Clear", font=("calibri", 14), command=clear)
clear_btn.grid(row=4, column=1)

start_window.mainloop()
