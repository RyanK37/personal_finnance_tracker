import tkinter as tk
from tkinter import ttk
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

# ===============================================================================================================================

def clear():                                                                     # Function to clear user input
    username_entry.delete(0, "end")
    password_entry.delete(0, tk.END)

# ===============================================================================================================================

def update_balance_label():                                                      # Update balance label in realtime
        balance.config(text="Current balance : " + str(account_balance))
    
# ===============================================================================================================================

def update_last_tran():                                                          # Update the latest transation in realtime
    if tran_data == []:
        last_tran_label.config(text="No transation currently!!")
    else:
        transation_string =""
        for data in tran_data:
            transation_string += str(data) + "\n"
        last_tran_label.config(text="Latest Transations : " + transation_string)

# ===============================================================================================================================      

def destroy_window(window):                                                     # destroy window according to parameter
    window.destroy()

# ===============================================================================================================================

def empty_transation_window():                                                  # To handle empty transations by prompting empty transation message window
    temp = tk.Tk()
    temp.title("Empty Transation")
    temp.geometry("400x100")
    empty_label = tk.Label(temp, text="There is no transation", font=("calibri", 14))
    empty_label.pack()
    temp.after(1500, lambda:destroy_window(temp))
    temp.mainloop()

# ===============================================================================================================================

def go_back(current, previous):                                                 # Go back to previous window
    current.destroy()
    previous.deiconify()
    
# ===============================================================================================================================

def update_tran_data(type, category, amount, date, source):                     # Update the transations in realtime
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

def filter_by_input(start, end, type, category, source):                        # Filter by time, type, category, source 
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

def filter_by_time(start, end, type):                                           # Filter by only time and type
    start_date = pd.to_datetime(start, format="%d-%b-%Y")
    end_date = pd.to_datetime(end, format="%d-%b-%Y")
        
    filtered_list = []
    for each_data in tran_data:
        if start_date <= pd.to_datetime(each_data["Date"], format="%d-%b-%Y") <= end_date and each_data["Type"] == type:
            filtered_list.append(each_data)
    return filtered_list

# ===============================================================================================================================

def draw_piechart(data_list, pie_data):                                         # Function to draw piecharts
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

def draw_barchart(data_list, bar_data):                                        # Function to draw barcharts
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

def write_file(data_list, filename):                                            # Function to handle Print button (writing datas in .txt file)
    if data_list == []:
        empty_transation_window()
    else:
        keys = list(data_list[0].keys())                                        # Getting the maximum width of each column
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
        with open(filename, 'w') as file:                                       # Writing the datas in table like format
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
        temp.after(1000, lambda:destroy_window(temp))
        temp.mainloop()   

# ===============================================================================================================================

def show_all_trans(window):                                                     # Function to show all transations
    window.withdraw()

    all_trans_window = tk.Tk()
    all_trans_window.title("All Transations")
    all_trans_window.geometry("1200x350")    
    
    for each in tran_data:                                                      # Print every transation
        each_label = tk.Label(all_trans_window, text=str(each), font=("calibri", 14))
        each_label.pack()
    
    # ---------------------------------------------------------------------------------
    
    def determine_pie():                                                        # Decide the numbers of pie chart to draw
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
    
    def determine_barchart():                                                   # Decide the numbers of bar chart to draw
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
    
    # ---------------------------------------------------------------------------------
    
    temp_frame = tk.Frame(all_trans_window)                                     # Frame to holld pie and bar chart buttons
    temp_frame.pack()
    
    pie_chart_btn = tk.Button(temp_frame, text="Pie Charts", font=("calibri", 14), command=determine_pie)
    pie_chart_btn.pack(side="left", padx=5, pady=5)
    
    bar_chart_btn = tk.Button(temp_frame, text="Bar Charts", font=("calibri", 14), command=determine_barchart)
    bar_chart_btn.pack(side="right", padx=5, pady=5)
    
    # ---------------------------------------------------------------------------------
    
    go_back_btn =  tk.Button(all_trans_window, text="Back", font=("calibri", 14), command=lambda: go_back(all_trans_window, window))
    go_back_btn.pack()
    # ---------------------------------------------------------------------------------
    
    all_trans_window.mainloop()
    
# ===============================================================================================================================
    
def piechart(previous_window):                                                  # Pie Chart Window from summary        
    previous_window.destroy()
    
    piechart_window = tk.Tk()
    piechart_window.geometry("500x400")
    piechart_window.title("Pie Chart")    
    
    # ---------------------------------------------------------------------------------    
    
    date_frame = tk.Frame(piechart_window)                                      # Frame to hold date entries
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
    
    radio_frame_pie = tk.Frame(piechart_window)                                     # Frame to hold type radiobuttons
    radio_frame_pie.pack()
    
    choose_type_pie = tk.StringVar(value="Income")
    income_radio_pie= tk.Radiobutton(radio_frame_pie, text="Income", variable=choose_type_pie, value="Income", font=("calibri", 14))
    income_radio_pie.pack(side="left")
    expense_radio_pie = tk.Radiobutton(radio_frame_pie, text="Expense", variable=choose_type_pie, value="Expense", font=("calibri", 14))
    expense_radio_pie.pack(side="right")
    
    # ---------------------------------------------------------------------------------    
    
    def draw_chart():                                                           # Draw the pie chart
        filtered_data = filter_by_time(date_range_from.get(), date_range_to.get(), choose_type_pie.get()) # get datas to draw pie chart
        if filtered_data == []:                                                # To handle empty transation
            temp_window = tk.Tk()
            temp_window.geometry("600x200")
            temp_window.title("Empty transation!")
            empty_alert = tk.Label(temp_window, text="There is no transation within the filtered range!!", font=("calibri", 16))
            empty_alert.pack()
            temp_window.mainloop()
        else:
            figure, pie_data = plt.subplots()                                 # Draw the pie chart
            draw_piechart(filtered_data, pie_data)
            plt.show()
    
    # ---------------------------------------------------------------------------------    
        
    draw_piechart_btn = tk.Button(piechart_window, text="Draw Pie Chart", font=("calibri", 14), command=draw_chart)
    draw_piechart_btn.pack()
    
    def go_back_summary():
        piechart_window.destroy()
        summary()
        
    go_back_btn =  tk.Button(piechart_window, text="Back", font=("calibri", 14), command=go_back_summary)
    go_back_btn.pack()
    
    piechart_window.mainloop()
    
# ===============================================================================================================================

def barchart(previous_window):                                                 # Bar Chart window from summary  
    previous_window.destroy()
    
    barchart_window = tk.Tk()
    barchart_window.geometry("500x400")
    barchart_window.title("Bar Chart")     
        
    # ---------------------------------------------------------------------------------    
    
    date_frame = tk.Frame(barchart_window)                                     # Frame to hold date entries
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
   
    radio_frame_bar = tk.Frame(barchart_window)                                     # Frame to hold type radiobuttons    
    radio_frame_bar.pack()
    
    choose_type_bar= tk.StringVar(value="Income")
    income_radio_bar = tk.Radiobutton(radio_frame_bar, text="Income", variable=choose_type_bar, value="Income", font=("calibri", 14))
    income_radio_bar.pack(side="left")
    expense_radio_bar = tk.Radiobutton(radio_frame_bar, text="Expense", variable=choose_type_bar, value="Expense", font=("calibri", 14))
    expense_radio_bar.pack(side="right")
                
    # ---------------------------------------------------------------------------------    
    
    def draw_chart():                                                       # Function to draw bar chart
        filtered_data = filter_by_time(date_range_from.get(), date_range_to.get(), choose_type_bar.get())  # Get datas for bar chart
        if filtered_data == []:                                                # Handle empty transation
            temp_window = tk.Tk()
            temp_window.geometry("600x200")
            temp_window.title("Empty transation!")
            empty_alert = tk.Label(temp_window, text="There is no transation within the filtered range!!", font=("calibri", 16))
            empty_alert.pack()
            temp_window.mainloop()
        else:                                                                  # Draw bar chart
            figure, bar_data = plt.subplots()
            draw_barchart(filtered_data, bar_data)
            plt.show()
                        
    # ---------------------------------------------------------------------------------    
        
    draw_barchart_btn = tk.Button(barchart_window, text="Draw Bar Chart", font=("calibri", 14), command=draw_chart)
    draw_barchart_btn.pack()
    
    def go_back_summary():
        barchart_window.destroy()
        summary()
        
    go_back_btn =  tk.Button(barchart_window, text="Back", font=("calibri", 14), command=go_back_summary)
    go_back_btn.pack()
    
    barchart_window.mainloop()
    
# ===============================================================================================================================

def summary():                                                                  # Dashborad Window function
    summary_window = tk.Tk()
    summary_window.geometry("700x400")
    summary_window.title("Dashboard")
                
    # ---------------------------------------------------------------------------------    
    
    date_frame = tk.Frame(summary_window)                                       # Frame to hold date entries
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
    
    radio_frame_summary = tk.Frame(summary_window)                                    # Frame to hold type radiobuttons
    radio_frame_summary.pack()
    
    choose_type_summary = tk.StringVar(value="Income")
    income_radio_summary = tk.Radiobutton(radio_frame_summary, text="Income", variable=choose_type_summary, value="Income", font=("calibri", 14))
    income_radio_summary.pack(side="left")
    expense_radio_summary = tk.Radiobutton(radio_frame_summary, text="Expense", variable=choose_type_summary, value="Expense", font=("calibri", 14))
    expense_radio_summary.pack(side="right")
                
    # ---------------------------------------------------------------------------------    
    
    option_frame = tk.Frame(summary_window)                                     # Frame to hold Dropdown category menu
    option_frame.pack()
    categories = {"Income": ["Salary", "Pension", "Interest"],        # Dropdown category menu
                  "Expense": ["Food", "Rent", "Clothing", "Car", "Health", "Others"]}
    category_real = tk.StringVar(value="Salary")
    
    category_label =tk.Label(option_frame, text="Category: ",  font=("calibri", 14))
    category_label.pack(side="left")
    category_menu = tk.OptionMenu(option_frame, category_real, *(categories["Income"] + categories["Expense"]))
    category_menu.pack(side="right")
    
    # ---------------------------------------------------------------------------------    
    
    source_label = tk.Label(summary_window, text="Payee/Source",  font=("calibri", 14))  # To get Payee/Source
    source_label.pack()
    source_entry = tk.Entry(summary_window)
    source_entry.pack()
    
    # ---------------------------------------------------------------------------------
    
    def show_filtered_data():                                                       # Function to show Filtered transations
        filtered_data = filter_by_input(date_range_from.get(), date_range_to.get(), choose_type_summary.get(), category_real.get(), source_entry.get())
        summary_window.withdraw()
        temp_window = tk.Tk()
        temp_window.title("Filterd transations")
        temp_window.geometry("800x500")
        
        if filtered_data == []:                                                     # For empty transations
            filtered_label = tk.Label(temp_window, text="There is no transation!!", font=("calibri", 14))
            filtered_label.pack()
        else:
            for each in filtered_data:                                              # Print filtered transtaions
                filtered_label = tk.Label(temp_window, text=str(each), font=("calibri", 14))
                filtered_label.pack()
                
        temp_frame = tk.Frame(temp_window)
        temp_frame.pack()
        print_btn = tk.Button(temp_frame, text="Print", font=("calibri", 14), command=lambda: write_file(filtered_data, "Filtered_Transations.txt"))    # To wrtie in .txt file
        print_btn.pack(side="left", padx=5, pady=5)
        
        go_back_btn =  tk.Button(temp_frame, text="Back", font=("calibri", 14), command=lambda: go_back(temp_window, summary_window)) # Go back to previous window
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
    
    barchart_btn = tk.Button(summary_window, text="Bar Chart", font=("calibri", 14), command=lambda: barchart(summary_window))  # Draw barchart
    barchart_btn.pack(padx=5, pady=5)
    
    piechart_btn = tk.Button(summary_window, text="Pie Chart",  font=("calibri", 14), command=lambda: piechart(summary_window)) # Draw Pie Chart
    piechart_btn.pack(padx=5, pady=5)
                
    # ---------------------------------------------------------------------------------    
    
    summary_window.mainloop()
        
# ===============================================================================================================================

def add_tran():                                                                  # Add Transations Window function
    global add_window
    add_window =tk.Tk()
    add_window.geometry("500x500")
    add_window.title("Add Transations")
    
    # ---------------------------------------------------------------------------------
    
    radio_frame = tk.Frame(add_window)                                          # Choose Income or Expense
    radio_frame.pack()
    
    choose_type = tk.StringVar(value="Income")
    income_radio = tk.Radiobutton(radio_frame, text="Income", variable=choose_type, value="Income", font=("calibri", 14))
    income_radio.pack(side="left")
    expense_radio = tk.Radiobutton(radio_frame, text="Expense", variable=choose_type, value="Expense", font=("calibri", 14))
    expense_radio.pack(side="right")
    
    # ---------------------------------------------------------------------------------
    category_frame = tk.Frame(add_window)                                      # Choose category
    category_frame.pack()
    categories = {"Income": ["Salary", "Pension", "Interest"],
                  "Expense": ["Food", "Rent", "Clothing", "Car", "Health", "Others"]}
    category_real = tk.StringVar(value="Salary")
    
    category_label =tk.Label(category_frame, text="Category:",  font=("calibri", 14))
    category_label.pack(side="left")
    category_menu = tk.OptionMenu(category_frame, category_real, *(categories["Income"] + categories["Expense"]))
    category_menu.pack(side="right")
       
    # ---------------------------------------------------------------------------------
     
    amount_label = tk.Label(add_window, text="Amount", font=("calibri", 14))  # Input amount
    amount_label.pack()
    amount_entry = tk.Entry(add_window)
    amount_entry.pack()
    
    date_label = tk.Label(add_window, text="Date(01-Apr-2004)",  font=("calibri", 14))  # Input date of transation
    date_label.pack()
    date_entry = tk.Entry(add_window)
    date_entry.pack()
    
    source_label = tk.Label(add_window, text="Payee/Source",  font=("calibri", 14))  # Payee/Source of transation
    source_label.pack()
    source_entry = tk.Entry(add_window)
    source_entry.pack()
        
    # ---------------------------------------------------------------------------------
    
    add_btn = tk.Button(add_window, text="Submit" , font=("calibri", 14), command=lambda : update_tran_data(choose_type.get(), category_real.get(), float(amount_entry.get()), date_entry.get(), source_entry.get()))
    add_btn.pack()
        
    # ---------------------------------------------------------------------------------
    
    add_window.mainloop()
    
# ===============================================================================================================================

def del_tran():                                                                     # Delete transation Window
    del_window = tk.Tk()
    del_window.geometry("300x300")
    del_window.title("Delete transations")
                
    # ---------------------------------------------------------------------------------    
    
    id_label = tk.Label(del_window, text="Please input ID to delete!")              # Input ID to delete transation
    id_label.pack()
    id_entry = tk.Entry(del_window)
    id_entry.pack()
                
    # ---------------------------------------------------------------------------------    
    
    def delete_update():                                                            # Update necessary datas after deleteing the transation
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

def main_window():                                                                  # The main window function
    main_window = tk.Tk()
    main_window.geometry("1200x400")
    main_window.title("Personal Finnace Tracker")
                
    # ---------------------------------------------------------------------------------    
    global user
    user = str(username_entry.get())
    welcome = tk.Label(main_window, text="Welcome " + user + "!" , font=("calibri", 14))  # Personalized Greeting
    welcome.pack()
    
    start_window.destroy()
                
    # ---------------------------------------------------------------------------------    
    global balance
    balance = tk.Label(main_window, text="Current balance : "  + str(account_balance), font=("calibri", 14))  # Initial Balance(zero)
    balance.pack()

    global last_tran_label
    last_tran_label = tk.Label(main_window, text="No transation currently!!!", font=("calibri", 14))  # Initial latest tran (which is none)
    last_tran_label.pack()
                
    # ---------------------------------------------------------------------------------    
    summarys_btn = tk.Button(main_window, text="Summary", font=("calibri", 14), command=summary)      # Go to dashboard Window
    summarys_btn.pack()
    
    add_tran_btn = tk.Button(main_window, text="Add transation", font=("calibri", 14), command=add_tran)    # Go to Add transations Window
    add_tran_btn.pack()
    
    del_tran_btn = tk.Button(main_window, text="Delete transation", font=("calibri" , 14), command=del_tran)    # Go to Delete transation window
    del_tran_btn.pack()
                
    # ---------------------------------------------------------------------------------    
    main_window.mainloop()
        
# ===============================================================================================================================

submit_icon = tk.Button(start_window, text="Submit", font=("calibri", 14), command=main_window)       # Go to main window
submit_icon.grid(row =4, column=0)

clear_btn = tk.Button(start_window, text="Clear", font=("calibri", 14), command=clear)     # Clear current input of username and password
clear_btn.grid(row=4, column=1)

start_window.mainloop()