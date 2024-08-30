from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from tkinter.ttk import OptionMenu
import win32api
from tkinter import filedialog
import mysql.connector
from sqlite3 import dbapi2 as sqlite
from log_maker import *
from tkinter import messagebox
from tkinter.tix import *
from math import ceil
import random
from datetime import date as dat

now = dat.today()
today_date = now

c=mysql.connector.connect(host="localhost" , user="root" , password="" , database="cfms")
cur=c.cursor()


def print_file():
    # Ask for file (Which you want to print)
    file_to_print = filedialog.askopenfilename(
        initialdir="/", title="Select file",
        filetypes=(("Text files", "*.txt"), ("all files", "*.*")))

    if file_to_print:
        # Print Hard Copy of File
        win32api.ShellExecute(0, "print", file_to_print, None, ".", 0)

def sell_insert():
    global middle_section, date, client, items, quantity, rate, total_var, paid
    print(date.get(), client.get(), items.get(), quantity.get(), rate.get(), total_var.get(), paid.get())

    success = True
    try:
        sql = "insert into sell(adate,client,item,quantity,rate,total,paid) values(date('%s'),'%s','%s',%s,%s,%s,'%s')" % (
        date.get(), client.get(), items.get(), quantity.get(), rate.get(), total_var.get(), paid.get())
        print(sql)
        cur.execute(sql)
        sql = "update stock_maintenance_payas set %s=%s-%i" % (items.get(),items.get(), quantity.get())
        print(sql)

        cur.execute(sql)

    except Exception as exp:
        print(exp)
        c.rollback()
        success = False
        insert_error(exp)
    if success:
        c.commit()
        insert_info("Sell Successfully Inserted")
        messagebox.showinfo('Successfull', 'Sell Successfully Inserted')
        get_last_sell()
        get_unpaid_sell()


def get_last_sell():
    global last_sell
    for widget in last_sell.winfo_children():
        widget.destroy()
    Label(last_sell, text="-" * 40 + "Last Five Sells" + "-" * 40, font=("Belwe Bd BT", 15), background="black",foreground="white").grid(
        row=1, column=1, columnspan=7)

    Label(last_sell, text="Date", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=1)
    Label(last_sell, text="Client", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=2)
    Label(last_sell, text="Type", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=3)
    Label(last_sell, text="Quantity", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=4)
    Label(last_sell, text="Rate", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=5)
    Label(last_sell, text="Total", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=6)
    Label(last_sell, text="Paid", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=7)

    try:
        sql = "select * from sell order by adate desc limit 5"
        print(sql)
        cur.execute(sql)
        i = 4
        for result in cur:
            Label(last_sell, text=result[1], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=1)
            Label(last_sell, text=result[2], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=2)
            Label(last_sell, text=result[3], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=3)
            Label(last_sell, text=result[4], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=4)
            Label(last_sell, text=result[5], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=5)
            Label(last_sell, text=result[6], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=6)
            Label(last_sell, text=result[7], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=7)
            i += 1
    except Exception as exp:
        insert_error(exp)

    Label(last_sell, text="-" * 80, font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=i, column=1, columnspan=7)


def update_sell(id):
    success = True
    try:
        sql = "update sell set paid='paid' where id=%s" % (id)
        print(sql)
        cur.execute(sql)
    except Exception as exp:
        print(exp)
        c.rollback()
        success = False
        insert_error(exp)
    if success:
        c.commit()
        insert_info("Sell Successfully Updated")
        messagebox.showinfo('Successfull', 'Sell Successfully Updated')
        get_last_sell()
        get_unpaid_sell()


def get_unpaid_sell():
    global unpaid_sell
    for widget in unpaid_sell.winfo_children():
        widget.destroy()
    Label(unpaid_sell, text="-" * 40 + "Unpaid Sells List" + "-" * 40, font=("Belwe Bd BT", 15),
          background="black",foreground="white").grid(row=1, column=1, columnspan=9)

    Label(unpaid_sell, text="Date", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=1)
    Label(unpaid_sell, text="Client", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=2)
    Label(unpaid_sell, text="Type", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=3)
    Label(unpaid_sell, text="Quantity", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=4)
    Label(unpaid_sell, text="Rate", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=5)
    Label(unpaid_sell, text="Total", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=6)
    Label(unpaid_sell, text="Action", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=7)

    try:
        sql = "select * from sell where paid='not paid' order by adate desc "
        print(sql)
        cur.execute(sql)
        i = 4
        for result in cur:
            Label(unpaid_sell, text=result[1], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=1)
            Label(unpaid_sell, text=result[2], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=2)
            Label(unpaid_sell, text=result[3], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=3)
            Label(unpaid_sell, text=result[4], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=4)
            Label(unpaid_sell, text=result[5], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=5)
            Label(unpaid_sell, text=result[6], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=6)
            tk.Button(unpaid_sell, text="Make Paid", font=("Belwe lt BT", 15),background="green",foreground="white",
                      command=lambda id=result[0]: update_sell(id)).grid(row=i, column=7)
            i += 1
    except Exception as exp:
        insert_error(exp)

    Label(unpaid_sell, text="-" * 80, font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=i + 1, column=1,
                                                                                         columnspan=7)


def calculate():
    global middle_section, last_sell, unpaid_sell, date, client, items, quantity, rate, total_var, paid, gst
    print(gst.get())
    if gst.get() == 1:
        total_var.set(round(int((quantity.get()) * rate.get() * 112) / 100, 2))
    else:
        total_var.set(round(int(quantity.get()) * rate.get(), 2))


def sell():
    global middle_section, last_sell, unpaid_sell, date, client, items, quantity, rate, total_var, paid, gst
    for widget in middle_section.winfo_children():
        widget.destroy()

    date = StringVar(middle_section, value=today_date)
    client = StringVar(middle_section)
    items = StringVar(middle_section)
    quantity = IntVar(middle_section)
    rate = DoubleVar(middle_section)
    total_var = DoubleVar(middle_section)
    paid = StringVar(middle_section)

    # Dictionary with options

    items_choices = ["Select Cashew", "A180","A210", "B320","B240", "C400","C440"]
    paid_choices = ["Select Option", "paid", "not paid"]

    date_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=date)
    Label(middle_section, text="Date", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=1)
    date_entry.grid(row=2, column=1)

    client_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=client)
    Label(middle_section, text="Client", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=2)
    client_entry.grid(row=2, column=2)

    items_option = ttk.OptionMenu(middle_section, items, *items_choices)
    Label(middle_section, text="Select Items", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=3)
    items_option.grid(row=2, column=3)

    quantity_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=quantity)
    Label(middle_section, text="Quantity", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=4)
    quantity_entry.grid(row=2, column=4)

    rate_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=rate)
    Label(middle_section, text="rate", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=5)
    rate_entry.grid(row=2, column=5)

    Label(middle_section, text="GST", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=6)

    gst = IntVar(middle_section)
    C1 = Checkbutton(middle_section, text="", variable=gst, onvalue=1, offvalue=0)
    C1.grid(row=2, column=6)

    Label(middle_section, text="Total", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=7,
                                                                                           columnspan=2)
    total_entry = Label(middle_section, font=("Belwe lt BT", 15), textvariable=total_var)
    tk.Button(middle_section, text="calculate", font=("Belwe lt BT", 15),background="green",foreground="white", command=lambda: calculate()).grid(row=2,
                                                                                                            column=8)
    total_entry.grid(row=2, column=7)

    paid_option = ttk.OptionMenu(middle_section, paid, *paid_choices)
    Label(middle_section, text="Paid/Not", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=9)
    paid_option.grid(row=2, column=9)

    items.set(items_choices[1])
    paid.set(paid_choices[1])

    tk.Button(middle_section, text="Add Sell", font=("Belwe Bd BT", 15),background="green",foreground="white", command=lambda: sell_insert()).grid(row=2,column=10)

    client_names = tk.Frame(middle_section)
    Label(client_names, text="-" * 10 + "Select Client Names From Here" + "-" * 10, font=("Belwe Bd BT", 15),
          background="black",foreground="white").pack(side=TOP)
    sql = "select name from clients"
    cur.execute(sql)

    def onmousewheel(event):
        print(event.delta)
        listbox1.yview('scroll', event.delta, 'units')
        return "break"

    def select_cn(e):
        name = listbox1.curselection()
        client.set(client_names_list[name[0]])
        print(listbox1)

    scrollbar = Scrollbar(client_names)

    listbox1 = Listbox(client_names, height=5)
    listbox1.pack()

    client_names_list = []

    for result in cur:
        listbox1.insert(END, result[0])
        client_names_list.append(result[0])

        # tk.Button(client_names,text=result[0],font=("Belwe lt BT",15),command=lambda name=result[0]: client.set(name) ).pack()
    listbox1.config(yscrollcommand=scrollbar.set)
    listbox1.bind('<MouseWheel>', onmousewheel)
    listbox1.bind('<<ListboxSelect>>', select_cn)

    client_names.grid(row=3, column=1, columnspan=2, sticky="W")

    # View Last Sells
    last_sell = tk.Frame(middle_section, background="black")

    get_last_sell()
    last_sell.grid(row=3, column=3, columnspan=7, sticky="E")

    # View unpaid Sells
    unpaid_sell = tk.Frame(middle_section, background="black")
    get_unpaid_sell()
    unpaid_sell.grid(row=6, column=1, columnspan=9, sticky="S")

def insert_raw_material():
    global middle_section,date,quantity,raw
    print(date.get(),raw.get(),quantity.get())
    success = True
    try:
        if raw.get()=='A':
            size='sa'
        if raw.get()=='B':
            size='sb'
        if raw.get()=='C':
            size='sc'


	
        sql = "insert into raw_material_payas(adate,raw,quantity) values(date('%s'),'%s',%i)"%(date.get(),raw.get(),quantity.get())
        cur.execute(sql)
        print(size)

        print(sql)
        sql = "update stock_maintenance set %s=%s-%i" % (size, size, quantity.get())
        cur.execute(sql)
        sql = "update stock_maintenance_payas set %s=%s+%i" % (size,size,quantity.get())
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
	




    Label(last_raw,text="Date",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=6,column=1)
    Label(last_raw,text="Cashew Type",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=6,column=2)
    Label(last_raw,text="Quantity",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=6,column=3)



    try:
        sql = "select * from raw_material_payas order by id desc"
        print(sql)
        cur.execute(sql)
        i=7
        for result in cur:

            Label(last_raw,text=result[1],background="black",foreground="white").grid(row=i,column=1)
            Label(last_raw,text=result[2],background="black",foreground="white").grid(row=i,column=2)
            Label(last_raw,text=result[3],background="black",foreground="white").grid(row=i,column=3)
            
            i+=1
    except Exception as exp:
        insert_error(exp)
    
    Label(last_raw,text="-"*80,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=i,column=1,columnspan=3)
	
def raw_material():
    global middle_section,last_raw,date,quantity,raw

    for widget in middle_section.winfo_children():
        widget.destroy()

    date = StringVar(middle_section,value=today_date)
    raw = StringVar(middle_section)
    quantity = IntVar(middle_section)	

    raw_choices = [ "","A","B","C"]
    raw.set(raw_choices[1]) # set the default option

	
	
    date_entry = Entry(middle_section,font=("Belwe lt BT",10),textvariable=date)
    Label(middle_section,text="Date",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=1,column=1)
    date_entry.grid(row=2,column=1)

    raw_option = ttk.OptionMenu(middle_section, raw, *raw_choices)
    Label(middle_section,text="Select Type",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=1,column=2)
    raw_option.grid(row=2,column=2)


    quantity_entry = Entry(middle_section,font=("Belwe lt BT",10),textvariable=quantity)
    Label(middle_section,text="Quantity",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=1,column=3)
    quantity_entry.grid(row=2,column=3)



    tk.Button(middle_section,text="Add Raw material",font=("Belwe Bd BT",15),background="green",foreground="white",command=lambda : insert_raw_material()).grid(row=2,column=5)
    Label(middle_section,text="-"*60+"Last Raw Material Entry"+"-"*60,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=3,columnspan=5)

    tk.Button(middle_section, text="Print", font=("Belwe Bd BT", 15),background="green",foreground="white",command=lambda: print_file()).grid(row=2, column=4)

    last_raw = tk.Frame(middle_section,background="black")
    
    get_last_raw()
	
    last_raw.grid(row=4,column=1,columnspan=4)
	
    

def production_insert():
    global middle_section,date,thousand,s1,s2,type,size,l1,l2
    print(size)
    print(size[0],size[1])
    total=s1.get()+s2.get()
    l1=size[0]
    l2=size[1]
    if type.get()=='A':
        st='sa'
    if type.get()=='B':
        st='sb'
    if type.get() == 'C':
        st = 'sc'
    print(type.get(),s1.get(),s2.get(),total)

    print(date.get(),type.get(),s1.get(),s2.get())
    success = True
    try:
        #sql = "insert into production_payas(adate,tf,fh,ts) values(date('%s'),%i,%i,%i)"%(date.get(),s1.get(),s2.get(),thousand.get())
        sql = "insert into production_payas(adate,type,size1,size2) values(date('%s'),'%s',%i,%i)"%(date.get(),type.get(),s1.get(),s2.get())
        cur.execute(sql)

        print(sql)		
        #sql = "update stock_maintenance_payas set tf=tf+%i,fh=fh+%i,ts=ts+%i,preformA=preformA-%f,preformB=preformB-%f,preformC=preformC-%f,lableA=lableA-%i,lableB=lableB-%i,lableC=lableC-%i,capsA=capsA-%i,capsB=capsB-%i,capsC=capsC-%i,boxesA=boxesA-%i,boxesB=boxesB-%i,boxesC=boxesC-%i"%(s1.get(),s2.get(),thousand.get(),pA,pB,p100,lA,lB,l100,cA,cB,c100,bA,bB,b100)
        sql = "update stock_maintenance_payas set %s=%s-%i,%s%s=%s%s+%i,%s%s=%s%s+%i" % (st, st,total, type.get(), l1, type.get(), l1,s1.get(),type.get(), l2, type.get(), l2,s2.get())
        #sql = "update stock_maintenance set %s=%s-%i,%s=%s+%i,%s=%s+%i" % (st, st,total,tel1,tel1,s1.get(),tel2,tel2,s2.get())

        print(sql)
        cur.execute(sql)
		
    except Exception as exp:
        print(exp)
        c.rollback()
        success = False
        insert_error(exp)
    if success:
        c.commit()
        insert_info("Production Successfully Inserted")
        messagebox.showinfo('Successfull', 'Production Successfully Inserted')
        get_last_production()

def get_last_production():
    global last_production
    for widget in last_production.winfo_children():
        widget.destroy()
    
	
    Label(last_production,text="-"*40+"Last Production"+"-"*40,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=1,column=1,columnspan=4)

		
    Label(last_production,text="Date",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=3,column=1)
    Label(last_production,text="TYPE",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=3,column=2)
    Label(last_production,text="Size",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=3,column=3)
    Label(last_production,text="Size",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=3,column=4)

    try:
        sql = "select * from production_payas order by adate desc"
        cur.execute(sql)
        i=4
        for result in cur:
            Label(last_production,text=result[0],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=1)
            Label(last_production,text=result[1],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=2)
            Label(last_production,text=result[2],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=3)
            Label(last_production,text=result[3],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=4)
            i+=1
			
    except Exception as exp:
        insert_error(exp)

    #Label(last_production,text="-"*80,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=14,column=1,columnspan=4)
    

def production():
    global middle_section,type,last_production,date,thousand,s1,s2,size

    for widget in middle_section.winfo_children():
        widget.destroy()
    s1 = IntVar(middle_section)
    s2 = IntVar(middle_section)
    type = StringVar(middle_section)
    date = StringVar(middle_section,value=today_date)

    type_choices = ["Select Type", "A", "B", "C"]
    size=["",""]


    date_entry = Entry(middle_section,font=("Belwe lt BT",10),textvariable=date)
    Label(middle_section,text="Date",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=1,column=1)
    date_entry.grid(row=2,column=1)

    type_option = ttk.OptionMenu(middle_section, type, *type_choices)
    Label(middle_section, text="Select Type", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=2)
    type_option.grid(row=2, column=2)
    print(type.get())
    def selects():
        global size
        if type.get() == "A":
            size[0] = "180"
            size[1] = "210"
        elif type.get() == 'B':
            size[0] = '240'
            size[1] = '320'
        elif type.get() == 'C':
            size[0] = '400'
            size[1] = '440'
        s1_entry = Entry(middle_section,font=("Belwe lt BT",10),textvariable=s1)
        Label(middle_section,text=size[0],font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=1,column=3)
        s1_entry.grid(row=2,column=3)

        s2_entry = Entry(middle_section,font=("Belwe lt BT",10),textvariable=s2)
        Label(middle_section,text=size[1],font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=1,column=4)
        s2_entry.grid(row=2,column=4)
    selects()


    tk.Button(middle_section,text="Add",font=("Belwe Bd BT",15),background="green",foreground="white",command=lambda : production_insert()).grid(row=2,column=5)

    tk.Button(middle_section, text="Refresh", font=("Belwe Bd BT", 15),background="green",foreground="white", command=lambda: selects()).grid(row=2,column=6)

    last_production = tk.Frame(middle_section,background="black")
    
    get_last_production()

	
	
    last_production.grid(row=4,column=1,columnspan=5)
	

	
	
	
	
def stock_maintain():
    global middle_section

    for widget in middle_section.winfo_children():
        widget.destroy()

		
    bottle_frame = tk.Frame(middle_section,background="black")
    Label(bottle_frame,text="-"*30+"Cashew"+"-"*30,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=1,column=1,columnspan=9)
    Label(bottle_frame,text="A",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2,column=1)
    Label(bottle_frame,text="B",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2,column=2)
    Label(bottle_frame,text="C",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2,column=3)
    Label(bottle_frame,text="A180",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2,column=4)
    Label(bottle_frame, text="A210", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=2, column=5)
    Label(bottle_frame, text="B320", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=2, column=6)
    Label(bottle_frame, text="B240", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=2, column=7)
    Label(bottle_frame, text="C400", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=2, column=8)
    Label(bottle_frame, text="C440", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=2, column=9)

    sql="select * from stock_maintenance_payas"
    cur.execute(sql)
    result = cur.fetchone()
    print(result)
    Label(bottle_frame, text=result[0], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=3, column=1)
    Label(bottle_frame, text=result[1], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=3, column=2)
    Label(bottle_frame, text=result[2], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=3, column=3)
    Label(bottle_frame, text=result[3], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=3, column=4)
    Label(bottle_frame, text=result[4], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=3, column=5)
    Label(bottle_frame, text=result[5], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=3, column=6)
    Label(bottle_frame, text=result[6], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=3, column=7)
    Label(bottle_frame, text=result[7], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=3, column=8)
    Label(bottle_frame, text=result[8], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=3, column=9)
    bottle_frame.grid(row=1,column=1,sticky="W",columnspan=9)

	


def main():
    ''' Payas GUI '''
    global middle_section
    flag='Payas'
    payas=Tk()
    payas.configure(background="black")
    payas.title('Grading')
    payas.state("zoomed")
    #billingsto.wm_iconbitmap('favicon.ico')
    #Label(payas,text='-'*48+'Grading'+'-'*49).grid(row=0,column=0,columnspan=7,sticky='W')
    
    side_menu = tk.Frame(payas,background="black")

    tk.Button(side_menu,width=20,text='Sell',font=("Belwe Bd BT",15),background="green",foreground="white",command=sell).grid(row=0, column=1)
    tk.Button(side_menu,width=20,text='RAW MATERIAL',font=("Belwe Bd BT",15),background="green",foreground="white",command=raw_material).grid(row=0, column=2)
    tk.Button(side_menu,width=20,text='PRODUCTION',font=("Belwe Bd BT",15),background="green",foreground="white",command=production).grid(row=0, column=3)
    tk.Button(side_menu,width=20,text='STOCK MAINTENANCE',font=("Belwe Bd BT",15),background="green",foreground="white",command=stock_maintain).grid(row=0, column=4)
    tk.Button(side_menu,width=20,text='Back to Main Menu',font=("Belwe Bd BT",15),background="green",foreground="white",command=payas.destroy).grid(row=0, column=5)
    Label(side_menu,text='-'*200,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2,column=1,columnspan=5,sticky='N')
	
    side_menu.pack(side=TOP)
    sw= ScrolledWindow(payas)
    sw.pack()

    middle_section = tk.Frame(sw.window,background="black")
    Label(middle_section,text='-'*48+'Grading'+'-'*49,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0,column=0,columnspan=9,sticky='N')
    middle_section.pack(fill=BOTH,expand=1)

    payas.mainloop()


    
def mainmenu():
    if flag=='sto':
        sto.destroy()
    elif flag=='billingsto':
        billingsto.destroy()  
    elif flag=='dailyinco':
        dailyinco.destroy()
        
main()