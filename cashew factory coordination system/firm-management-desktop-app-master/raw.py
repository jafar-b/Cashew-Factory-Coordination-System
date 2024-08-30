from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from sqlite3 import dbapi2 as sqlite
from log_maker import *
from tkinter import messagebox
from tkinter.tix import *
from math import ceil
import random
from datetime import date as dat
import mysql.connector

now = dat.today()
today_date = now
columns = ('Item_No', 'Item_Name', 'Item_Type', 'Quantity_Remain', 'Item_Cost', 'Expiry_Date', 'Manufactured_By')

c = mysql.connector.connect(host="localhost", user="root", password="", database="cfms")
cur = c.cursor()


def submit():
    return 0


def insert_raw_material():
    global middle_section, date, quantity, raw
    print(date.get(), quantity.get())
    success = True
    try:

        sql = "insert into raw_material(adate,raw,quantity) values(date('%s'),'%s',%i)" % (
        date.get(), raw.get(), quantity.get())
        cur.execute(sql)

        print(sql)
        sql = "update stock_maintenance set %s=%s+%i" % (raw.get(),raw.get(), quantity.get())
        print(sql)
        cur.execute(sql)

    except Exception as exp:
        print(exp)
        c.rollback()
        success = False
        insert_error(exp)
    if success:
        c.commit()
        insert_info("Raw Material Successfully Inserted")
        messagebox.showinfo('Successfull', 'Raw Material Successfully Inserted')
        get_last_raw()


def get_last_raw():
    global last_raw

    for widget in last_raw.winfo_children():
        widget.destroy()

    Label(last_raw, text="Date", font=("Belwe Bd BT", 15), background="white").grid(row=6, column=1)
    Label(last_raw, text="Bottle", font=("Belwe Bd BT", 15), background="white").grid(row=6, column=2)
    Label(last_raw, text="Type", font=("Belwe Bd BT", 15), background="white").grid(row=6, column=3)
    Label(last_raw, text="Quantity", font=("Belwe Bd BT", 15), background="white").grid(row=6, column=4)

    try:
        sql = "select * from raw_material order by id desc"
        print(sql)
        cur.execute(sql)
        i = 7
        for result in cur:
            Label(last_raw, text=result[1], background="white").grid(row=i, column=1)
            Label(last_raw, text=result[2], background="white").grid(row=i, column=2)
            Label(last_raw, text=result[3], background="white").grid(row=i, column=3)
            Label(last_raw, text=result[4], background="white").grid(row=i, column=4)

            i += 1
    except Exception as exp:
        insert_error(exp)

    Label(last_raw, text="-" * 80, font=("Belwe Bd BT", 15), background="white").grid(row=i, column=1, columnspan=4)


def raw_material():
    global middle_section, last_raw, date, type, quantity, raw

    for widget in middle_section.winfo_children():
        widget.destroy()

    date = StringVar(middle_section, value=today_date)
    type = StringVar(middle_section)
    raw = StringVar(middle_section)
    quantity = IntVar(middle_section)

    type_choices = ["", "preform", "caps", "lable", "boxes"]
    type.set(type_choices[1])  # set the default option
    raw_choices = ["", "A", "500", "1000"]
    raw.set(raw_choices[1])  # set the default option

    date_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=date)
    Label(middle_section, text="Date", font=("Belwe Bd BT", 15), background="white").grid(row=1, column=1)
    date_entry.grid(row=2, column=1)

    raw_option = ttk.OptionMenu(middle_section, raw, *raw_choices)
    Label(middle_section, text="Select Bootle", font=("Belwe Bd BT", 15), background="white").grid(row=1, column=2)
    raw_option.grid(row=2, column=2)

    type_option = ttk.OptionMenu(middle_section, type, *type_choices)
    Label(middle_section, text="Select Type", font=("Belwe Bd BT", 15), background="white").grid(row=1, column=3)
    type_option.grid(row=2, column=3)

    quantity_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=quantity)
    Label(middle_section, text="Quantity", font=("Belwe Bd BT", 15), background="white").grid(row=1, column=4)
    quantity_entry.grid(row=2, column=4)

    tk.Button(middle_section, text="Add Raw material", font=("Belwe Bd BT", 15),
              command=lambda: insert_raw_material()).grid(row=2, column=5)
    Label(middle_section, text="-" * 60 + "Last Raw Material Entry" + "-" * 60, font=("Belwe Bd BT", 15),
          background="white").grid(row=3, columnspan=5)

    last_raw = tk.Frame(middle_section, background="white")

    get_last_raw()

    last_raw.grid(row=4, column=1, columnspan=4)




