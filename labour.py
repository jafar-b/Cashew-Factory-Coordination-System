from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
from tkinter.tix import *
from PIL import ImageTk, Image
import mysql.connector

from sqlite3 import dbapi2 as sqlite
from log_maker import *
import time


c=mysql.connector.connect(host="localhost" , user="root" , password="" , database="cfms")
cur=c.cursor()




def addBox():
    global entry_frame,name,other

    # I use len(all_entries) to get nuber of next free column
    next_row = len(name)


    # add entry in second row
    name.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    name[next_row].grid(row=next_row+1, column=1)
    other.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    other[next_row].grid(row=next_row+1, column=2)

def insert_labour():
    global name,other
    success = True
    try:
        for i in range(len(name)):
            sql = "insert into labour_details(name,other) values('%s','%s')"%(name[i].get(),other[i].get())
            cur.execute(sql)
    except Exception as exp:
        c.rollback()
        success = False




        insert_error(exp)
    if success:
        c.commit()
        insert_info("Labours Successfully Inserted")
        messagebox.showinfo('Successfull', 'Labours Successfully Inserted')
        get_labour()
'''
def delete_row(name):
    print(name)
    success = True
    try:
        sql="delete from labour_details where id=%s"%(name)
        cur.execute(sql)
        get_labour()
    except Exception as exp:
        insert_error(exp)
    if success:
        c.commit()
        insert_info("labour Successfully Deleted")
        messagebox.showinfo('Successfull', 'labor Details Deleted')
        '''
def get_labour():
    global labour_view

    for widget in labour_view.winfo_children():
        widget.destroy()
    Label(labour_view,text="-"*80,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=1,column=1,columnspan=2)
    Label(labour_view,text="Name",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2,column=1)
    Label(labour_view,text="Other Information",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2,column=2)

    try:
        sql = "select name,other from labour_details"
        cur.execute(sql)
        i=4
        for result in cur:
            Label(labour_view,text=result[0],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=1)
            Label(labour_view,text=result[1],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=2)
            #tk.Button(labour_view, width=15, text='Delete', font=("Belwe lt BT", 15),command=lambda item=result[0]: delete_row(item)).grid(row=i, column=3)
            i+=1
    except Exception as exp:
        insert_error(exp)
    Label(labour_view,text="-"*80,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=14,column=1,columnspan=2)

def add_labour():
    global flag,entry_frame,labour_view,name,other
    flag='add_labour'

    add_labour=Tk()
    add_labour.configure(background="black")
    add_labour.state("zoomed")
    add_labour.title('Add labour Details')
    add_labour.bg = ImageTk.PhotoImage(file="background.png")
    add_labour.bg_image = Label(add_labour, image=add_labour.bg).place(x=0, y=0, relwidth=1, relheight=1)

    sw= ScrolledWindow(add_labour)
    sw.pack()


    full_labour_frame = tk.Frame(sw.window,background="black")
    column_frame = tk.Frame(full_labour_frame,background="black")

    #full_labour_frame.wm_iconbitmap('favicon.ico')
    Label(column_frame,text='-'*80,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2, column=0,columnspan=3)

    column_frame.pack(anchor=CENTER)

    entry_frame = tk.Frame(full_labour_frame,background="black")
    Label(entry_frame,text="Name",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0, column=1)
    Label(entry_frame,text="Other Information",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0, column=2)

    name = []
    other = []
    i=0
    name.append(Entry(entry_frame,font=("Belwe lt BT",15), relief=GROOVE))
    name[i].grid(row=i+1, column=1)
    other.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    other[i].grid(row=i+1, column=2)

    entry_frame.pack(anchor=CENTER)

    button_frame = tk.Frame(full_labour_frame,background="black")
    Label(button_frame,text="",background="black",foreground="white").grid(row=0, column=0)
    tk.Button(button_frame,width=10,font=("Belwe Bd BT",15),background="green",foreground="white",text='Add Box',command=addBox).grid(row=1, column=0)
    tk.Button(button_frame,width=15,font=("Belwe Bd BT",15),background="green",foreground="white",text='Insert Details',command=lambda:insert_labour()).grid(row=1, column=2)
    tk.Button(button_frame,width=20,font=("Belwe Bd BT",15),background="green",foreground="white",text='Return to Main Menu',command=add_labour.destroy).grid(row=1, column=4)

    button_frame.pack(anchor=CENTER)

    labour_view = tk.Frame(full_labour_frame,background="black")

    get_labour()


    labour_view.pack(anchor=CENTER)
    full_labour_frame.pack(fill=BOTH,expand=1)
    add_labour.mainloop()




def mainmenu():
    if flag=='expirychk':
        expirychk.destroy()



# expiry()
#view_labour()