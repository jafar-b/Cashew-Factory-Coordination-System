from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from sqlite3 import dbapi2 as sqlite
from math import ceil
import random
from datetime import date as dat
import mysql.connector
from tkinter import messagebox

# Constants and Database Connection
now = dat.today()
today_date = now
columns = ('Item_No', 'Item_Name', 'Item_Type', 'Quantity_Remain', 'Item_Cost', 'Expiry_Date', 'Manufactured_By')

# Database connection
try:
    c = mysql.connector.connect(
        host="localhost",
        user="Admin",
        password="newpassword123",
        database="cfms"
    )
    cur = c.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
    exit()


class ScrolledWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#f5f5f5", highlightthickness=0)
        self.frame = tk.Frame(self.canvas, background="#f5f5f5")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.frame.pack(fill="both", expand=True)


def calculate():
    global quantity, rate, total_var, gst
    try:
        if gst.get() == 1:
            total_var.set(round(int((quantity.get()) * rate.get() * 112) / 100, 2))
        else:
            total_var.set(round(int(quantity.get()) * rate.get(), 2))
    except Exception as e:
        messagebox.showerror("Calculation Error", f"Error in calculation: {e}")


def sell_insert():
    global date, client, items, quantity, rate, total_var, paid, region

    if not all([date.get(), client.get(), items.get(), quantity.get(), rate.get(), region.get()]):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        sql = "INSERT INTO sell (adate, client, item, quantity, rate, total, paid, region) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
        date.get(), client.get(), items.get(), quantity.get(), rate.get(), total_var.get(), paid.get(), region.get())
        cur.execute(sql, values)

        item_type = items.get()
        if item_type not in ['A', 'B', 'C']:
            raise ValueError("Invalid item type")

        column = f"s{item_type.lower()}"
        update_sql = f"UPDATE stock_maintenance SET {column} = {column} - %s"
        cur.execute(update_sql, (quantity.get(),))

        update_sql = f"UPDATE stock_maintenance SET {region.get()}{item_type} = {region.get()}{item_type} - %s"
        cur.execute(update_sql, (quantity.get(),))

        log_sql = "INSERT INTO stock_changes (region, cashew_type, `change`) VALUES (%s, %s, %s)"
        log_values = (region.get(), item_type, f"-{quantity.get()}")
        cur.execute(log_sql, log_values)

        c.commit()
        messagebox.showinfo('Success', 'Sale Successfully Recorded')
        get_last_sell()
        get_unpaid_sell()
        stock_maintain()

    except Exception as exp:
        print(exp)
        c.rollback()
        messagebox.showerror('Error', f'An error occurred: {exp}')


def get_last_sell():
    global last_sell

    for widget in last_sell.winfo_children():
        widget.destroy()

    # Main container frame
    container = tk.Frame(last_sell, bg="#f5f5f5")
    container.pack(expand=True, fill="both", padx=20, pady=10)

    # Header frame
    header_frame = tk.Frame(container, bg="#3a7ca5")
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="Last Five Sales", font=("Arial", 12, "bold"),
             bg="#3a7ca5", fg="white", padx=10, pady=5).pack()

    # Table frame
    table_frame = tk.Frame(container, bg="#f5f5f5")
    table_frame.pack(expand=True, fill="both")

    # Configuring grid columns to center content
    for i in range(8):  # 8 columns
        table_frame.grid_columnconfigure(i, weight=1)

    # Column headers
    headers = ["Date", "Client", "Size", "Type", "Quantity", "Rate", "Total", "Paid"]
    for col, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Arial", 10, "bold"),
                 bg="#2f6690", fg="white", padx=10, pady=5).grid(row=0, column=col, sticky="ew")

    try:
        sql = "SELECT adate, client, item, quantity, rate, total, paid, region FROM sell ORDER BY adate DESC LIMIT 5"
        cur.execute(sql)

        # Displaying data with correct column mapping
        for row_idx, result in enumerate(cur, start=1):
            # Mapping of database columns to display columns:
            # 0: adate (Date)
            # 1: client (Client)
            # 2: item (Size)
            # 7: region (Type)
            # 3: quantity (Quantity)
            # 4: rate (Rate)
            # 5: total (Total)
            # 6: paid (Paid)

            date = result[0]
            client = result[1]
            size = result[2]
            cashew_type = result[7]  # region field
            quantity = result[3]
            rate = result[4]
            total = result[5]
            paid_status = result[6]

            # Creating the display row
            display_values = [date, client, size, cashew_type, quantity, rate, total, paid_status]

            for col, value in enumerate(display_values):
                tk.Label(table_frame, text=value, font=("Arial", 10),
                         bg="#d9dcd6", padx=10, pady=5).grid(row=row_idx, column=col, sticky="ew")

    except Exception as exp:
        messagebox.showerror("Database Error", f"Error fetching sales: {exp}")


def update_sell(id):
    try:
        sql = "update sell set paid='paid' where id=%s" % (id)
        cur.execute(sql)
        c.commit()
        messagebox.showinfo('Success', 'Sale Marked as Paid')
        get_last_sell()
        get_unpaid_sell()
    except Exception as exp:
        c.rollback()
        messagebox.showerror('Error', f'An error occurred: {exp}')


def get_unpaid_sell():
    global unpaid_sell

    # Clearing existing widgets
    for widget in unpaid_sell.winfo_children():
        widget.destroy()

    # Main container frame
    container = tk.Frame(unpaid_sell, bg="#f5f5f5")
    container.pack(expand=True, fill="both", padx=20, pady=10)

    # Header frame
    header_frame = tk.Frame(container, bg="#3a7ca5")
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="Unpaid Sales List", font=("Arial", 12, "bold"),
             bg="#3a7ca5", fg="white", padx=10, pady=5).pack()

    # Table frame
    table_frame = tk.Frame(container, bg="#f5f5f5")
    table_frame.pack(expand=True, fill="both")

    # Configuring grid columns to center content
    for i in range(8):  # 8 columns (7 data columns + 1 action column)
        table_frame.grid_columnconfigure(i, weight=1)

    # Column headers
    headers = ["Date", "Client", "Size", "Type", "Quantity", "Rate", "Total", "Action"]
    for col, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Arial", 10, "bold"),
                 bg="#2f6690", fg="white", padx=10, pady=5).grid(row=0, column=col, sticky="ew")

    try:
        sql = "SELECT id, adate, client, item, quantity, rate, total, region FROM sell WHERE paid='not paid' ORDER BY adate DESC"
        cur.execute(sql)

        # Displaying data with correct column mapping
        for row_idx, result in enumerate(cur, start=1):
            # Mapping the database columns to display columns:
            # 0: id (used for the action button)
            # 1: adate (Date)
            # 2: client (Client)
            # 3: item (Size)
            # 7: region (Type)
            # 4: quantity (Quantity)
            # 5: rate (Rate)
            # 6: total (Total)

            sale_id = result[0]
            date = result[1]
            client = result[2]
            size = result[3]
            cashew_type = result[7]
            quantity = result[4]
            rate = result[5]
            total = result[6]

            # Creating the display row
            display_values = [date, client, size, cashew_type, quantity, rate, total]

            for col, value in enumerate(display_values):
                tk.Label(table_frame, text=value, font=("Arial", 10),
                         bg="#d9dcd6", padx=10, pady=5).grid(row=row_idx, column=col, sticky="ew")

            # Adding action button in the last column
            btn = tk.Button(table_frame, text="Mark Paid", font=("Arial", 10),
                            command=lambda id=sale_id: update_sell(id),
                            bg="#4CAF50", fg="white")
            btn.grid(row=row_idx, column=7, sticky="ew", padx=5, pady=5)

    except Exception as exp:
        messagebox.showerror("Database Error", f"Error fetching unpaid sales: {exp}")


def insert_raw_material():
    global date, item_type, quantity, raw

    if not all([date.get(), item_type.get(), quantity.get(), raw.get()]):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        sql = "INSERT INTO raw_material (adate, raw, item_type, quantity) VALUES (%s, %s, %s, %s)"
        values = (date.get(), raw.get(), item_type.get(), quantity.get())
        cur.execute(sql, values)
        c.commit()
        messagebox.showinfo('Success', 'Raw Material Successfully Recorded')
        get_last_raw()
    except Exception as exp:
        print(exp)
        c.rollback()
        messagebox.showerror('Error', f'An error occurred: {exp}')


def get_last_raw():
    global last_raw

    for widget in last_raw.winfo_children():
        widget.destroy()

    # Main container frame that will center everything
    main_container = tk.Frame(last_raw, bg="#f5f5f5")
    main_container.pack(expand=True, fill="both", padx=20, pady=20)

    # Configuring the main container to center its contents
    main_container.grid_columnconfigure(0, weight=1)
    main_container.grid_rowconfigure(0, weight=1)

    # Content frame that will hold all elements
    content_frame = tk.Frame(main_container, bg="#f5f5f5")
    content_frame.grid(row=0, column=0, sticky="nsew")

    # Header frame
    header_frame = tk.Frame(content_frame, bg="#3a7ca5")
    header_frame.pack(fill="x", pady=(0, 10))
    tk.Label(header_frame, text="Recent Raw Material Entries", font=("Arial", 12, "bold"),
             bg="#3a7ca5", fg="white", padx=10, pady=5).pack()

    # Table container frame - to center the table
    table_container = tk.Frame(content_frame, bg="#f5f5f5")
    table_container.pack(expand=True, fill="both")

    # Actual table frame
    table_frame = tk.Frame(table_container, bg="#f5f5f5")
    table_frame.pack(expand=True)  # This centers the table in the container

    # Column headers
    headers = ["Date", "Cashew", "Type", "Quantity"]
    for col, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Arial", 10, "bold"),
                 bg="#2f6690", fg="white", padx=10, pady=5, width=15).grid(
            row=0, column=col, sticky="ew", padx=1, pady=1)

    try:
        sql = "SELECT * FROM raw_material ORDER BY id DESC LIMIT 12"
        cur.execute(sql)

        # Displaying data
        for row_idx, result in enumerate(cur, start=1):
            for col, value in enumerate(result[1:5]):  # Skipping id column
                tk.Label(table_frame, text=value, font=("Arial", 10),
                         bg="#d9dcd6", padx=10, pady=5, width=15).grid(
                    row=row_idx, column=col, sticky="ew", padx=1, pady=1)

    except Exception as exp:
        messagebox.showerror("Database Error", f"Error fetching raw materials: {exp}")


def production_insert():
    global date, item_type, sa, sb, sc

    if not all([date.get(), item_type.get()]) or not any([sa.get(), sb.get(), sc.get()]):
        messagebox.showerror("Error", "All fields are required and at least one quantity!")
        return

    try:
        sql = "INSERT INTO production (adate, item_type, sa, sb, sc) VALUES (%s, %s, %s, %s, %s)"
        values = (date.get(), item_type.get(), sa.get(), sb.get(), sc.get())
        cur.execute(sql, values)

        region = item_type.get()
        for size, qty in [('A', sa.get()), ('B', sb.get()), ('C', sc.get())]:
            if qty > 0:
                update_sql = f"UPDATE stock_maintenance SET s{size.lower()} = s{size.lower()} + %s"
                cur.execute(update_sql, (qty,))

                update_sql = f"UPDATE stock_maintenance SET {region}{size} = {region}{size} + %s"
                cur.execute(update_sql, (qty,))

                log_sql = "INSERT INTO stock_changes (region, cashew_type, `change`) VALUES (%s, %s, %s)"
                log_values = (region, size, f"+{qty}")
                cur.execute(log_sql, log_values)

        c.commit()
        messagebox.showinfo('Success', 'Production Successfully Recorded')
        get_last_production()
        stock_maintain()
    except Exception as exp:
        print(exp)
        c.rollback()
        messagebox.showerror('Error', f'An error occurred: {exp}')


def get_last_production():
    global last_production

    for widget in last_production.winfo_children():
        widget.destroy()

    # Main container frame
    container = tk.Frame(last_production, bg="#f5f5f5")
    container.pack(expand=True, fill="both", padx=20, pady=10)

    # Header frame
    header_frame = tk.Frame(container, bg="#3a7ca5")
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="Recent Production Entries", font=("Arial", 12, "bold"),
             bg="#3a7ca5", fg="white", padx=10, pady=5).pack()

    # Table frame
    table_frame = tk.Frame(container, bg="#f5f5f5")
    table_frame.pack(expand=True, fill="both")

    # Configuring grid columns to center content
    for i in range(5):  # 5 columns
        table_frame.grid_columnconfigure(i, weight=1)

    # Column headers
    headers = ["Date", "Type", "A", "B", "C"]
    for col, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Arial", 10, "bold"),
                 bg="#2f6690", fg="white", padx=10, pady=5).grid(row=0, column=col, sticky="ew")

    try:
        sql = "SELECT * FROM production ORDER BY adate DESC LIMIT 10"
        cur.execute(sql)

        # Display data
        for row_idx, result in enumerate(cur, start=1):
            display_order = [result[0], result[4], result[1], result[2], result[3]]
            for col, value in enumerate(display_order):
                tk.Label(table_frame, text=value, font=("Arial", 10),
                         bg="#d9dcd6", padx=10, pady=5).grid(row=row_idx, column=col, sticky="ew")

    except Exception as exp:
        messagebox.showerror("Database Error", f"Error fetching production: {exp}")


def update_stock():
    try:
        cur.execute("SELECT * FROM stock_maintenance")
        result = cur.fetchone()

        regions = ["Kokan", "African", "Benin", "Ghana"]
        sizes = ["A", "B", "C"]
        columns = [f"{region}{size}" for region in regions for size in sizes]
        values = [input_fields[col].get() for col in columns]

        if not result:
            sql = f"INSERT INTO stock_maintenance ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
        else:
            sql = f"UPDATE stock_maintenance SET {', '.join([f'{col}=%s' for col in columns])}"
            for col in columns:
                old_value = result[3 + columns.index(col)]
                new_value = input_fields[col].get()
                if new_value != old_value:
                    cur.execute("INSERT INTO stock_changes (region, cashew_type, `change`) VALUES (%s, %s, %s)",
                                (col[:-1], col[-1], f"{old_value} -> {new_value}"))

        cur.execute(sql, values)
        c.commit()
        messagebox.showinfo('Success', 'Stock Successfully Updated')
        stock_maintain()
    except Exception as exp:
        print(exp)
        c.rollback()
        messagebox.showerror('Error', f'An error occurred: {exp}')


def get_stock_changes():
    global changes_frame

    for widget in changes_frame.winfo_children():
        widget.destroy()

    # Main container frame using grid
    container = tk.Frame(changes_frame, bg="#f5f5f5")
    container.pack(expand=True, fill="both", padx=20, pady=10)

    # Header frame using grid
    header_frame = tk.Frame(container, bg="#3a7ca5")
    header_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

    tk.Label(header_frame, text="Recent Stock Changes", font=("Arial", 12, "bold"),
             bg="#3a7ca5", fg="white", padx=10, pady=5).pack()

    # Column headers using grid
    headers = ["Region", "Type", "Change", "Timestamp"]
    for col, header in enumerate(headers):
        tk.Label(container, text=header, font=("Arial", 10, "bold"),
                 bg="#2f6690", fg="white", padx=10, pady=5).grid(
            row=1, column=col, sticky="ew")

    try:
        sql = "SELECT region, cashew_type, `change`, timestamp FROM stock_changes ORDER BY timestamp DESC LIMIT 6"
        cur.execute(sql)

        for row_idx, result in enumerate(cur, start=2):
            for col, value in enumerate(result):
                tk.Label(container, text=value, font=("Arial", 10),
                         bg="#d9dcd6", padx=10, pady=5).grid(
                    row=row_idx, column=col, sticky="ew")

        # Configuring column weights
        for col in range(4):
            container.grid_columnconfigure(col, weight=1)

    except Exception as exp:
        messagebox.showerror("Database Error", f"Error fetching stock changes: {exp}")


def sell():
    global middle_section, last_sell, unpaid_sell, date, client, items, quantity, rate, total_var, paid, gst, region

    for widget in middle_section.winfo_children():
        widget.destroy()

    date = StringVar(middle_section, value=today_date)
    client = StringVar(middle_section)
    items = StringVar(middle_section)
    quantity = IntVar(middle_section)
    rate = DoubleVar(middle_section)
    total_var = DoubleVar(middle_section)
    paid = StringVar(middle_section)
    region = StringVar(middle_section)
    gst = IntVar(middle_section)

    items_choices = ["Select Cashew", "A", "B", "C"]
    paid_choices = ["Select Option", "paid", "not paid"]
    region_choices = ["Select Region", "Kokan", "African", "Benin", "Ghana"]

    # Configuring grid weights
    middle_section.grid_columnconfigure(0, weight=1)
    middle_section.grid_columnconfigure(1, weight=3)
    middle_section.grid_rowconfigure(0, weight=0)
    middle_section.grid_rowconfigure(1, weight=1)
    middle_section.grid_rowconfigure(2, weight=0)

    # Input Frame - Extended to full width
    input_frame = tk.Frame(middle_section, background="#f5f5f5", padx=10, pady=10)
    input_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # Configuring input frame columns to use available space
    for i in range(11):
        input_frame.grid_columnconfigure(i, weight=1)

    # Date
    Label(input_frame, text="Date", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=0, sticky="w")
    date_entry = Entry(input_frame, font=("Arial", 11), textvariable=date)
    date_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    # Client
    Label(input_frame, text="Client", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=1, sticky="w")
    client_entry = Entry(input_frame, font=("Arial", 11), textvariable=client)
    client_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    # Region
    Label(input_frame, text="Select Type", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=2, sticky="w")
    region_option = ttk.OptionMenu(input_frame, region, *region_choices)
    region_option.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
    region.set(region_choices[1])

    # Items
    Label(input_frame, text="Select Size", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=3, sticky="w")
    items_option = ttk.OptionMenu(input_frame, items, *items_choices)
    items_option.grid(row=1, column=3, sticky="ew", padx=5, pady=5)
    items.set(items_choices[1])

    # Quantity
    Label(input_frame, text="Quantity", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=4, sticky="w")
    quantity_entry = Entry(input_frame, font=("Arial", 11), textvariable=quantity)
    quantity_entry.grid(row=1, column=4, sticky="ew", padx=5, pady=5)

    # Rate
    Label(input_frame, text="Rate", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=5, sticky="w")
    rate_entry = Entry(input_frame, font=("Arial", 11), textvariable=rate)
    rate_entry.grid(row=1, column=5, sticky="ew", padx=5, pady=5)

    # GST
    Label(input_frame, text="GST", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=6, sticky="w")
    C1 = Checkbutton(input_frame, variable=gst, onvalue=1, offvalue=0)
    C1.grid(row=1, column=6, sticky="w", padx=5, pady=5)

    # Total
    Label(input_frame, text="Total", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=7, sticky="w")
    total_entry = Label(input_frame, font=("Arial", 11), textvariable=total_var,
                        background="white", relief="sunken", width=15)
    total_entry.grid(row=1, column=7, sticky="ew", padx=5, pady=5)

    # Calculate Button
    btn = tk.Button(input_frame, text="Calculate", font=("Arial", 11),
                    command=calculate, bg="#4CAF50", fg="white")
    btn.grid(row=1, column=8, sticky="ew", padx=5, pady=5)

    # Paid/Not Paid
    Label(input_frame, text="Paid/Not", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=9, sticky="w")
    paid_option = ttk.OptionMenu(input_frame, paid, *paid_choices)
    paid_option.grid(row=1, column=9, sticky="ew", padx=5, pady=5)
    paid.set(paid_choices[1])

    # Add Sell Button
    btn = tk.Button(input_frame, text="Add Sale", font=("Arial", 11),
                    command=sell_insert, bg="#2196F3", fg="white")
    btn.grid(row=1, column=10, sticky="ew", padx=5, pady=5)

    # Client List
    client_frame = tk.Frame(middle_section, background="#f5f5f5", padx=10, pady=10)
    client_frame.grid(row=1, column=0, sticky="nsew")

    Label(client_frame, text="Select Client Names", font=("Arial", 12, "bold"),
          background="#f5f5f5").pack(side=TOP, pady=5)

    scrollbar = Scrollbar(client_frame)
    scrollbar.pack(side="right", fill="y")

    listbox1 = Listbox(client_frame, yscrollcommand=scrollbar.set,
                       font=("Arial", 11), background="white")
    listbox1.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox1.yview)

    try:
        # Clearing existing list
        listbox1.delete(0, END)

        # Forcing fresh query
        cur.execute("COMMIT")  # Ensuring any pending transactions are completed
        cur.execute("SELECT name FROM clients")

        # Repopulating listbox
        for client_name in cur:
            listbox1.insert(END, client_name[0])
            listbox1.insert(END, "-" * 90)

        def select_client(e):
            selection = listbox1.curselection()
            if selection:
                selected = listbox1.get(selection[0])
                if selected and not selected.startswith("-"):
                    client.set(selected)

        listbox1.bind("<<ListboxSelect>>", select_client)

    except Exception as exp:
        messagebox.showerror("Error", f"Could not load clients: {exp}")

    except Exception as exp:
        messagebox.showerror("Error", f"Could not load clients: {exp}")

    # Sales Tables
    tables_frame = tk.Frame(middle_section, background="#f5f5f5")
    tables_frame.grid(row=1, column=1, sticky="nsew")
    tables_frame.grid_rowconfigure(0, weight=1)
    tables_frame.grid_rowconfigure(1, weight=1)
    tables_frame.grid_columnconfigure(0, weight=1)

    # Last Sales
    last_sell = tk.Frame(tables_frame, background="#f5f5f5")
    last_sell.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
    get_last_sell()

    # Unpaid Sales
    unpaid_sell = tk.Frame(tables_frame, background="#f5f5f5")
    unpaid_sell.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    get_unpaid_sell()


def raw_material():
    global middle_section, last_raw, date, item_type, quantity, raw

    for widget in middle_section.winfo_children():
        widget.destroy()

    date = StringVar(middle_section, value=today_date)
    item_type = StringVar(middle_section)
    raw = StringVar(middle_section)
    quantity = IntVar(middle_section)

    item_type_choices = ["Select Type", "Kokan", "Benin", "African", "Ghana"]
    raw_choices = ["Select Size", "A", "B", "C"]

    # Configuring middle section to expand properly
    middle_section.grid_columnconfigure(0, weight=1)
    middle_section.grid_rowconfigure(0, weight=0)
    middle_section.grid_rowconfigure(1, weight=1)

    # Main container frame for centering
    container = tk.Frame(middle_section, background="#f5f5f5")
    container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    container.grid_columnconfigure(0, weight=1)

    # Input Frame - Centered with max width
    input_frame = tk.Frame(container, background="#f5f5f5", padx=10, pady=10)
    input_frame.grid(row=0, column=0, sticky="nsew")

    # Configuring input frame columns to use available space
    for i in range(5):
        input_frame.grid_columnconfigure(i, weight=1)

    # Date
    Label(input_frame, text="Date", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=0, sticky="w")
    date_entry = Entry(input_frame, font=("Arial", 11), textvariable=date)
    date_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    # Size
    Label(input_frame, text="Select Size", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=1, sticky="w")
    raw_option = ttk.OptionMenu(input_frame, raw, *raw_choices)
    raw_option.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    raw.set(raw_choices[0])

    # Type
    Label(input_frame, text="Select Type", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=2, sticky="w")
    item_type_option = ttk.OptionMenu(input_frame, item_type, *item_type_choices)
    item_type_option.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
    item_type.set(item_type_choices[0])

    # Quantity
    Label(input_frame, text="Quantity", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=3, sticky="w")
    quantity_entry = Entry(input_frame, font=("Arial", 11), textvariable=quantity)
    quantity_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

    # Add Button
    btn = tk.Button(input_frame, text="Add Raw Material", font=("Arial", 11),
                    command=insert_raw_material, bg="#2196F3", fg="white")
    btn.grid(row=1, column=4, sticky="ew", padx=5, pady=5)

    # Recent Entries
    last_raw = tk.Frame(container, background="#f5f5f5", padx=20, pady=10)
    last_raw.grid(row=1, column=0, sticky="nsew")
    last_raw.grid_columnconfigure(0, weight=1)

    get_last_raw()


def production():
    global middle_section, last_production, date, sa, sb, sc, item_type

    for widget in middle_section.winfo_children():
        widget.destroy()

    sa = IntVar(middle_section)
    sb = IntVar(middle_section)
    sc = IntVar(middle_section)
    date = StringVar(middle_section, value=today_date)
    item_type = StringVar(middle_section)

    middle_section.grid_columnconfigure(0, weight=1)
    middle_section.grid_rowconfigure(0, weight=0)
    middle_section.grid_rowconfigure(1, weight=1)

    # Input Frame - Extended to full width
    input_frame = tk.Frame(middle_section, background="#f5f5f5", padx=10, pady=10)
    input_frame.grid(row=0, column=0, sticky="nsew")

    # Configuring input frame columns to use available space
    for i in range(6):
        input_frame.grid_columnconfigure(i, weight=1)

    # Date
    Label(input_frame, text="Date", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=0, sticky="w")
    date_entry = Entry(input_frame, font=("Arial", 11), textvariable=date)
    date_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    # Type
    type_choices = ["Select Type", "Kokan", "African", "Benin", "Ghana"]
    Label(input_frame, text="Select Type", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=1, sticky="w")
    type_option = ttk.OptionMenu(input_frame, item_type, *type_choices)
    type_option.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    item_type.set(type_choices[0])

    # A, B, C
    Label(input_frame, text="A", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=2, sticky="w")
    sa_entry = Entry(input_frame, font=("Arial", 11), textvariable=sa)
    sa_entry.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

    Label(input_frame, text="B", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=3, sticky="w")
    sb_entry = Entry(input_frame, font=("Arial", 11), textvariable=sb)
    sb_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

    Label(input_frame, text="C", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=4, sticky="w")
    sc_entry = Entry(input_frame, font=("Arial", 11), textvariable=sc)
    sc_entry.grid(row=1, column=4, sticky="ew", padx=5, pady=5)

    # Add Button
    btn = tk.Button(input_frame, text="Add", font=("Arial", 11),
                    command=production_insert, bg="#2196F3", fg="white")
    btn.grid(row=1, column=5, sticky="ew", padx=5, pady=5)

    # Recent Entries
    last_production = tk.Frame(middle_section, background="#f5f5f5", padx=20, pady=10)
    last_production.grid(row=1, column=0, sticky="nsew")
    get_last_production()


def stock_maintain():
    global middle_section, input_fields, changes_frame

    for widget in middle_section.winfo_children():
        widget.destroy()

    # Configuring middle section layout
    middle_section.grid_columnconfigure(0, weight=1)
    middle_section.grid_rowconfigure(0, weight=1)
    middle_section.grid_rowconfigure(1, weight=1)

    # Stock Frame - using grid
    stock_frame = tk.Frame(middle_section, bg="#f5f5f5", padx=20, pady=10)
    stock_frame.grid(row=0, column=0, sticky="nsew")
    stock_frame.grid_columnconfigure(0, weight=1)

    # Header frame - using pack inside its own frame
    header_container = tk.Frame(stock_frame, bg="#f5f5f5")
    header_container.pack(fill="x")

    header_frame = tk.Frame(header_container, bg="#3a7ca5")
    header_frame.pack(fill="x")

    tk.Label(header_frame, text="Current Stock Levels", font=("Arial", 12, "bold"),
            bg="#3a7ca5", fg="white", padx=10, pady=5).pack()

    try:
        cur.execute("SELECT * FROM stock_maintenance")
        result = cur.fetchone()

        input_fields = {}
        regions = ["Kokan", "African", "Benin", "Ghana"]
        sizes = ["A", "B", "C"]

        # Table frame - using grid
        table_frame = tk.Frame(stock_frame, bg="#f5f5f5")
        table_frame.pack(expand=True, fill="both")

        # Column headers - using grid
        tk.Label(table_frame, text="Region", font=("Arial", 10, "bold"),
                bg="#2f6690", fg="white", padx=10, pady=5).grid(
                row=1, column=0, sticky="ew")

        for col, size in enumerate(sizes, start=1):
            tk.Label(table_frame, text=size, font=("Arial", 10, "bold"),
                    bg="#2f6690", fg="white", padx=10, pady=5).grid(
                    row=1, column=col, sticky="ew")

        # Input fields - using grid
        for row_idx, region in enumerate(regions, start=2):
            tk.Label(table_frame, text=region, font=("Arial", 10),
                    bg="#d9dcd6", padx=10, pady=5).grid(
                    row=row_idx, column=0, sticky="ew")

            for col_idx, size in enumerate(sizes, start=1):
                col_name = f"{region}{size}"
                value = result[3 + (row_idx - 2) * 3 + (col_idx - 1)] if result else 0

                var = IntVar(value=value)
                tk.Entry(table_frame, textvariable=var, font=("Arial", 10),
                        justify="center", bg="white").grid(
                        row=row_idx, column=col_idx, sticky="ew", padx=5, pady=5)
                input_fields[col_name] = var

        # Configuring table columns
        for col in range(4):
            table_frame.grid_columnconfigure(col, weight=1)

        # Update button - using pack
        btn_frame = tk.Frame(stock_frame, bg="#f5f5f5")
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Update Stock", font=("Arial", 11),
                command=update_stock, bg="#4CAF50", fg="white").pack()

    except Exception as exp:
        messagebox.showerror("Error", f"Could not load stock: {exp}")

    # Changes Frame - using grid
    changes_frame = tk.Frame(middle_section, bg="#f5f5f5", padx=20, pady=10)
    changes_frame.grid(row=1, column=0, sticky="nsew")
    get_stock_changes()


def main():
    global middle_section

    root = tk.Tk()
    root.title("Cashew Factory Coordination System")
    root.state("zoomed")
    root.configure(bg="#f5f5f5")

    # Style configuration
    style = ttk.Style()
    style.theme_use('clam')

    # Configuring styles
    style.configure('TFrame', background='#f5f5f5')
    style.configure('TButton',
                    foreground='white',
                    background='#4CAF50',
                    bordercolor='#4CAF50',
                    lightcolor='#4CAF50',
                    darkcolor='#45a049',
                    relief='flat',
                    padding=5)
    style.map('TButton',
              background=[('active', '#45a049')],
              foreground=[('active', 'white')])

    style.configure('TLabel',
                    font=('Arial', 10),
                    foreground='#333',
                    background='#f5f5f5',
                    padding=5)
    style.configure('TEntry',
                    fieldbackground='white',
                    foreground='#333',
                    insertcolor='black',
                    relief='sunken')
    style.configure('TMenubutton',
                    font=('Arial', 10),
                    foreground='#333',
                    background='#f5f5f5',
                    relief='raised')

    # Menu
    side_menu = tk.Frame(root, bg="#333", padx=10, pady=10)
    side_menu.pack(side="top", fill="x")

    buttons = [
        ('SALES', sell),
        ('RAW MATERIAL', raw_material),
        ('PRODUCTION', production),
        ('STOCK MAINTENANCE', stock_maintain),
        ('EXIT', root.destroy)
    ]

    for idx, (text, command) in enumerate(buttons):
        if text == "EXIT":
            btn = tk.Button(side_menu, text=text, command=command,
                            font=("Arial", 11, "bold"), bg="#e74c3c", fg="white")
        else:
            btn = tk.Button(side_menu, text=text, command=command,
                            font=("Arial", 11, "bold"), bg="#3498db", fg="white")

        btn.grid(row=0, column=idx, padx=5, pady=5, sticky="ew")
        side_menu.grid_columnconfigure(idx, weight=1)

    # Scrollable Middle Section
    sw = ScrolledWindow(root)
    sw.pack(fill="both", expand=True)

    # Middle Section inside the Scrollable Frame
    middle_section = tk.Frame(sw.frame, background="#f5f5f5")
    middle_section.pack(fill="both", expand=True)

    # Initial welcome message
    Label(middle_section, text="Please select the Domain",
          font=("Arial", 14, "bold"), background="#f5f5f5").pack(expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()