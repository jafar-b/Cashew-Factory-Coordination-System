from tkinter import *
import tkinter as tk
import tkinter as ttk
import mysql.connector
import qrcode
from PIL import ImageTk, Image
from tkinter.ttk import *
from datetime import datetime, timedelta
from tkinter import Label, Frame, Button
from expenses import month
from log_maker import *
from datetime import date, timedelta
from tkinter import messagebox
import demand_prediction
import os
import payas
import tkinter as tk
from tkinter import ttk
from cashew_backup_system import BackupSystem

# Database connection
login = mysql.connector.connect(host="localhost", user="Admin", password="newpassword123", database="cfms")
l = login.cursor()
WinStat = ''
root = None
application = None
create_window = None
forgot_window = None

# Date calculations
now = date.today()
today_date = now
yesterday = now - timedelta(days=1)
y = yesterday
last_fifteen = now - timedelta(days=15)
f = last_fifteen


def future_choice():
    application.destroy()
    import future_choice
    a = future_choice.main()
    open_win()


def payas():
    application.destroy()
    import payas
    a = payas.main()
    open_win()


def edit_expenses():
    application.destroy()
    import expenses
    a = expenses.edit_daylist()
    open_win()


def view_expenses():
    application.destroy()
    import expenses
    a = expenses.view_daylist()
    open_win()


def labour_details():
    application.destroy()
    import labour
    a = labour.add_labour()
    open_win()


def attendance():
    application.destroy()
    import attendance_register
    a = attendance_register.main()
    open_win()


def ot():
    application.destroy()
    import ot
    a = ot.main()
    open_win()


def labour_payment():
    application.destroy()
    import make_payment
    a = make_payment.main()
    open_win()


def add_clients():
    application.destroy()
    import clients
    a = clients.add_client()
    open_win()


def view_clients():
    application.destroy()
    import clients
    a = clients.view_clients()
    open_win()

def signup():
    u = un.get()
    p = pwd.get()
    q = question_var.get()
    a = ans.get()
    result = False

    if u == "" or p == "" or q == "" or a == "":
        messagebox.showwarning("Warning", "Please fill all fields to create your account")
    else:
        try:
            sql = "insert into user values('%s','%s','%s','%s')" % (u, p, q, a)
            l.execute(sql)
            login.commit()
            result = True
        except:
            result = False

    if result:
        messagebox.showinfo("Success", "Account created successfully!")
    else:
        messagebox.showerror("Error", "Account could not be created. Username may already exist.")


# Enhanced forgot password window
def forgot_pass():
    global root, forgot_window, WinStat, un, question_var, ans

    if root:
        root.destroy()

    WinStat = 'forgot_window'
    forgot_window = tk.Tk()
    forgot_window.title("Recover Password - Sawant Cashew Industries")
    forgot_window.state("zoomed")

    # Set background image
    bg_image = Image.open("cashewb.jpg")
    bg_image = bg_image.resize((forgot_window.winfo_screenwidth(), forgot_window.winfo_screenheight()), Image.LANCZOS)
    forgot_window.bg = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(forgot_window, image=forgot_window.bg)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Main container
    main_container = tk.Frame(forgot_window, bg="#ffffff")
    main_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Main frame
    forgot_main_frame = tk.Frame(main_container, bg="white", padx=30, pady=30)
    forgot_main_frame.pack(padx=5, pady=5)

    # Company logo
    img = Image.open('sawant.jpg')
    img = img.resize((300, 200))
    img_photo = ImageTk.PhotoImage(img)
    logo_label = tk.Label(forgot_main_frame, image=img_photo, bg="white")
    logo_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

    # Title
    title_label = tk.Label(forgot_main_frame, text='Password Recovery',
                           font=("Verdana", 24, "bold"), foreground="#8B4513",
                           background="white")
    title_label.grid(row=1, column=0, columnspan=4, pady=(0, 10))

    subtitle_label = tk.Label(forgot_main_frame,
                              text='Please enter your details to recover your password',
                              font=("Verdana", 12), foreground="#A0522D",
                              background="white")
    subtitle_label.grid(row=2, column=0, columnspan=4, pady=(0, 15))

    # Divider
    divider = tk.Frame(forgot_main_frame, height=2, bg="#D2B48C")
    divider.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(0, 20))

    # Input fields
    tk.Label(forgot_main_frame, text='Username', font=("Verdana", 12),
             background="white", foreground="#8B4513").grid(row=4, column=0,
                                                            sticky="w", pady=10)
    un = tk.Entry(forgot_main_frame, font=("Verdana", 12), width=20,
                  bd=2, relief=tk.GROOVE)
    un.grid(row=4, column=1, padx=20, pady=10)

    tk.Label(forgot_main_frame, text='Security Question', font=("Verdana", 12),
             background="white", foreground="#8B4513").grid(row=5, column=0,
                                                            sticky="w", pady=10)

    question_var = tk.StringVar()
    choices = ['First Employee number you assigned?', 'Your first ever Business Trip?']
    question_var.set(choices[1])
    question_menu = tk.OptionMenu(forgot_main_frame, question_var, *choices)
    question_menu.config(width=18, font=("Verdana", 11))
    question_menu.grid(row=5, column=1, padx=20, pady=10, sticky="w")

    tk.Label(forgot_main_frame, text='Answer', font=("Verdana", 12),
             background="white", foreground="#8B4513").grid(row=6, column=0,
                                                            sticky="w", pady=10)
    ans = tk.Entry(forgot_main_frame, font=("Verdana", 12), width=20,
                   bd=2, relief=tk.GROOVE)
    ans.grid(row=6, column=1, padx=20, pady=10)

    # Button frame
    button_frame = tk.Frame(forgot_main_frame, bg="white")
    button_frame.grid(row=7, column=0, columnspan=4, pady=20)

    # Buttons
    recover_btn = tk.Button(button_frame, text='Recover Password',
                            font=("Verdana", 12, "bold"), width=18,
                            command=get_pass, bg="#8B4513", fg="white",
                            activebackground="#D2B48C", activeforeground="white",
                            relief=tk.RAISED, bd=2)
    recover_btn.grid(row=0, column=0, padx=10)

    back_btn = tk.Button(button_frame, text='Back to Login',
                         font=("Verdana", 12, "bold"), width=14,
                         command=again, bg="#A52A2A", fg="white",
                         activebackground="#CD5C5C", activeforeground="white",
                         relief=tk.RAISED, bd=2)
    back_btn.grid(row=0, column=1, padx=10)

    # Bottom divider
    divider2 = tk.Frame(forgot_main_frame, height=2, bg="#D2B48C")
    divider2.grid(row=8, column=0, columnspan=4, sticky="ew", pady=20)

    # Maintaining image references
    forgot_main_frame.img_photo = img_photo
    forgot_window.mainloop()


def get_pass():
    u = un.get()
    q = question_var.get()
    a = ans.get()
    password = ""

    # Predefined answers for the questions
    predefined_answers = {
        'First Employee number you assigned?': '30',
        'Your first ever Business Trip?': 'Kerala'
    }

    if u == "" or q == "" or a == "":
        messagebox.showwarning("Warning", "Please Fill All The Details")
    else:
        # Verify the answer against the predefined answers
        if predefined_answers.get(q) == a:
            try:
                # Retrieve the password from the database based on the username
                sql = "SELECT * FROM user WHERE username='%s'" % (u)
                l.execute(sql)
            except Exception as e:
                print("Error executing SQL:", e)
                messagebox.showerror("Error", "Database error")

            count = 0
            for i in l:
                password = i[1]

            if password != "":
                messagebox.showinfo("Password Recovery", "Your Password is: " + password)
            else:
                messagebox.showerror("Error", "User not found or incorrect details")
        else:
            # If the answer is wrong
            messagebox.showerror("Error", "Incorrect security answer, please try again.")


# Login window
def again():
    global root, application, create_window, forgot_window, WinStat, un, pwd

    # Destroying previous windows if they exist
    if WinStat == 'application':
        application.destroy()
    elif WinStat == 'create_window':
        create_window.destroy()
    elif WinStat == 'forgot_window':
        forgot_window.destroy()

    # Creating main window
    root = tk.Tk()
    root.title('Sawant Cashew Industries - Login')
    root.state("zoomed")

    # Background image
    bg_image = Image.open("cashewb.jpg")
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    root.bg = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=root.bg)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Main container
    container_frame = tk.Frame(root, bg="white", bd=2, relief=tk.GROOVE)
    container_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Login frame
    login_frame = tk.Frame(container_frame, bg="white", padx=40, pady=30)
    login_frame.pack()

    # Company logo
    img = Image.open('sawant.jpg')
    img = img.resize((300, 200))
    my = ImageTk.PhotoImage(img)
    panel = tk.Label(login_frame, image=my, bg="white")
    panel.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # Title
    tk.Label(login_frame, text='Welcome to Sawant Cashew Industries',
          font=("Verdana", 18, "bold"), fg="#8B4513", bg="white"
          ).grid(row=1, column=0, columnspan=2, pady=(0, 10))

    tk.Label(login_frame, text='Please login to continue',
          font=("Verdana", 12), fg="#A0522D", bg="white"
          ).grid(row=2, column=0, columnspan=2, pady=(0, 20))

    # Divider
    tk.Frame(login_frame, height=2, bg="#D2B48C"
          ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 25))

    # Username
    tk.Label(login_frame, text='USERNAME', font=("Verdana", 12),
          bg="white", fg="#8B4513").grid(row=4, column=0, sticky="w", pady=5)

    un = tk.Entry(login_frame, font=("Verdana", 12), width=25,
                  bd=2, relief=tk.GROOVE, highlightbackground="#D2B48C",
                  highlightthickness=1)
    un.grid(row=4, column=1, pady=5)

    # Password
    tk.Label(login_frame, text='PASSWORD', font=("Verdana", 12),
          bg="white", fg="#8B4513").grid(row=5, column=0, sticky="w", pady=5)

    pwd = tk.Entry(login_frame, font=("Verdana", 12), width=25, show="*",
                   bd=2, relief=tk.GROOVE, highlightbackground="#D2B48C",
                   highlightthickness=1)
    pwd.grid(row=5, column=1, pady=5)

    # Login button
    login_btn = tk.Button(login_frame, text='LOGIN', font=("Verdana", 14, "bold"),
                       width=20, command=check, bg="#8B4513", fg="white",
                       activebackground="#A0522D", relief=tk.RAISED, bd=2)
    login_btn.grid(row=6, column=0, columnspan=2, pady=25)

    # Divider
    tk.Frame(login_frame, height=2, bg="#D2B48C"
          ).grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 15))

    # Forgot password
    forgot_btn = tk.Button(login_frame, text='Forgot Password?',
                        font=("Verdana", 10, "underline"), bg="white",
                        fg="#0000FF", bd=0, relief=tk.FLAT, command=forgot_pass)
    forgot_btn.grid(row=8, column=0, columnspan=2, pady=(0, 10))

    # Create account
    #tk.Label(login_frame, text="Don't have an account?", font=("Verdana", 10),
         # bg="white").grid(row=9, column=0, sticky="e", pady=(10, 0))

    #create_btn = tk.Button(login_frame, text='Create Account',
                       # font=("Verdana", 10, "underline"), bg="white",
                      #  fg="#0000FF", bd=0, relief=tk.FLAT, command=create_account)
   # create_btn.grid(row=9, column=1, sticky="w", pady=(10, 0))

    # Storing image references
    login_frame.my_img = my
    login_frame.bg_img = root.bg

    root.bind("<Return>", check)
    root.mainloop()


def check(event=None):
    u = un.get()
    p = pwd.get()

    if u == "" or p == "":
        messagebox.showwarning('Warning', 'Please enter your username and password')
    else:
        try:
            sql = "select * from user where username='%s' and password='%s'" % (u, p)
            l.execute(sql)
        except Exception as e:
            print("SQL Error:", e)

        count = 0
        for i in l:
            count += 1

        if count > 0:
            root.destroy()
            open_win()
        else:
            messagebox.showerror('Error', 'Invalid username or password')


def open_win():
    ''' Opens Main Window '''
    global application, WinStat
    import mysql.connector
    import tkinter as tk
    from tkinter import Tk, Label, Menu, BOTH, FLAT, X, Y, RIGHT, LEFT, BOTTOM, CENTER, GROOVE, RIDGE, SUNKEN
    from tkinter import ttk
    from PIL import Image, ImageTk
    from datetime import datetime, timedelta

    con = mysql.connector.connect(host="localhost", user="Admin", password="newpassword123", database="cfms")
    cur = con.cursor()

    WinStat = 'application'
    application = Tk()

    BackupSystem.init_system()

    application.title("Sawant Cashew Industries - Management System")
    application.geometry("1200x700")
    application.configure(background="#FFF8DC")  #Cornsilk colour
    application.state("zoomed")


    # Creating a style for the application
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme as base

    # Configuring colors for various widget elements
    style.configure('TFrame', background='#FFF8DC')
    style.configure('TLabel', background='#FFF8DC', font=('Roboto', 11))
    style.configure('TButton', background='#8B5A2B', foreground='white', font=('Roboto', 11, 'bold'))
    style.map('TButton', background=[('active', '#A0522D')])

    # Main container with padding
    main_container = tk.Frame(application, bg="#FFF8DC", padx=20, pady=20)
    main_container.pack(fill=BOTH, expand=1)

    # Header frame with company name and logo
    header_frame = tk.Frame(main_container, bg="#FFF8DC", pady=10)
    header_frame.pack(fill=X)

    # Company title
    title_label = tk.Label(header_frame,
                           text="CASHEW FACTORY COORDINATION SYSTEM",
                           font=("Georgia", 28, "bold"),
                           fg="#8B4513",  # SaddleBrown - earthy tone matching cashew theme
                           bg="#FFF8DC",
                           pady=10)
    title_label.pack()

    # Subtitle
    subtitle_label = tk.Label(header_frame,
                              text="Information Management System",
                              font=("Georgia", 14),
                              fg="#A0522D",  # Sienna - complementary to SaddleBrown
                              bg="#FFF8DC",
                              pady=5)
    subtitle_label.pack()

    # Main content area with 3-column layout
    content_frame = tk.Frame(main_container, bg="#FFF8DC")
    content_frame.pack(fill=BOTH, expand=1, pady=10)

    # Left sidebar with image
    left_sidebar = tk.Frame(content_frame, bg="#FFF8DC", padx=10, pady=10, relief=tk.RIDGE, bd=1)
    left_sidebar.pack(side=LEFT, fill=Y, padx=10)

    #cashew image
    b_img = ImageTk.PhotoImage(Image.open('cashew.jpg'))
    left_img_label = tk.Label(left_sidebar, image=b_img, bg="#FFF8DC", relief=tk.GROOVE, bd=2)
    left_img_label.image = b_img  # Keep reference to prevent garbage collection
    left_img_label.pack(pady=10)

    # Center area with main content
    center_area = tk.Frame(content_frame, bg="#FFF8DC", padx=15, pady=15, relief=tk.RIDGE, bd=1)
    center_area.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

    img = ImageTk.PhotoImage(Image.open('collage.jpg'))
    img_container = tk.Frame(center_area, bg="#FFF8DC", relief=tk.SUNKEN, bd=2)
    img_container.pack(fill=X, pady=10)

    img_label = tk.Label(img_container, image=img, bg="#FFF8DC")
    img_label.image = img
    img_label.pack(pady=5)


    menu_bar = Menu(application, tearoff=0, font=("Roboto", 12), bg="#FFF8DC", activebackground="#D2B48C",
                    activeforeground="black")

    # Defining menus with modern styling
    bottle = Menu(menu_bar, tearoff=0, font=("Roboto", 11), bg="#FFF8DC", fg="#8B4513",
                  activebackground="#D2B48C", activeforeground="black")
    labour = Menu(menu_bar, tearoff=0, font=("Roboto", 11), bg="#FFF8DC", fg="#8B4513",
                  activebackground="#D2B48C", activeforeground="black")
    manage_clients = Menu(menu_bar, tearoff=0, font=("Roboto", 11), bg="#FFF8DC", fg="#8B4513",
                          activebackground="#D2B48C", activeforeground="black")
    expenses = Menu(menu_bar, tearoff=0, font=("Roboto", 11), bg="#FFF8DC", fg="#8B4513",
                    activebackground="#D2B48C", activeforeground="black")

    # Adding commands to the menus with separators for grid-like spacing
    bottle.add_command(label="Splitting", command=future_choice)
    bottle.add_separator()
    bottle.add_command(label="Reports", command=payas)

    labour.add_command(label="Employee Details", command=labour_details)
    labour.add_separator()
    labour.add_command(label="Attendance", command=attendance)
    labour.add_separator()
    labour.add_command(label="Over Time", command=ot)
    labour.add_separator()
    labour.add_command(label="Salary", command=labour_payment)

    expenses.add_command(label="Enter Expenses", command=edit_expenses)
    expenses.add_separator()
    expenses.add_command(label="View Expenses", command=view_expenses)

    manage_clients.add_command(label="Add Clients", command=add_clients)
    manage_clients.add_separator()
    manage_clients.add_command(label="View Clients", command=view_clients)

    # Adding menus to the menu bar
    menu_bar.add_cascade(label="Cashew", menu=bottle)
    menu_bar.add_cascade(label="Employee", menu=labour)
    menu_bar.add_cascade(label="Expenses", menu=expenses)
    menu_bar.add_cascade(label="Manage Clients", menu=manage_clients)
    menu_bar.add_cascade(label="Logout", command=again)

    application.config(menu=menu_bar)

    dashboard_frame = tk.Frame(center_area, bg="#FFF8DC")
    dashboard_frame.pack(fill=BOTH, expand=True, pady=10)


    canvas = tk.Canvas(dashboard_frame, bg="#FFF8DC", highlightthickness=0)
    canvas.pack(fill=BOTH, expand=True)

    for i in range(100):
        color = '#{:02x}{:02x}{:02x}'.format(255 - i // 2, 248 - i // 2, 220 - i // 2)
        canvas.create_line(0, i, 2000, i, fill=color)

    # Frames for the three data panels
    # Last Day Expenses Panel
    expenses_panel = tk.Frame(dashboard_frame, bg="#FFF8E0", padx=15, pady=15, relief=tk.GROOVE, bd=2)
    expenses_panel.place(relx=0.02, rely=0.05, relwidth=0.3, relheight=0.85)

    expenses_title = tk.Label(expenses_panel, text="Last Day Expenses", font=("Georgia", 16, "bold"),
                              bg="#FFF8E0", fg="#8B4513", pady=5)
    expenses_title.pack(anchor=tk.CENTER, pady=5)

    expenses_separator = ttk.Separator(expenses_panel, orient='horizontal')
    expenses_separator.pack(fill=X, pady=5)

    expenses_content = tk.Frame(expenses_panel, bg="#FFF8E0")
    expenses_content.pack(fill=BOTH, expand=True, pady=5)

    # Last Day Sale Panel
    sales_panel = tk.Frame(dashboard_frame, bg="#FFF8E0", padx=15, pady=15, relief=tk.GROOVE, bd=2)
    sales_panel.place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.85)

    sales_title = tk.Label(sales_panel, text="Last Day Sale", font=("Georgia", 16, "bold"),
                           bg="#FFF8E0", fg="#8B4513", pady=5)
    sales_title.pack(anchor=tk.CENTER, pady=5)

    sales_separator = ttk.Separator(sales_panel, orient='horizontal')
    sales_separator.pack(fill=X, pady=5)

    sales_content = tk.Frame(sales_panel, bg="#FFF8E0")
    sales_content.pack(fill=BOTH, expand=True, pady=5)

    # Payment Pending Panel
    pending_panel = tk.Frame(dashboard_frame, bg="#FFF8E0", padx=15, pady=15, relief=tk.GROOVE, bd=2)
    pending_panel.place(relx=0.68, rely=0.05, relwidth=0.3, relheight=0.85)

    pending_title = tk.Label(pending_panel, text="Payment Pending", font=("Georgia", 16, "bold"),
                             bg="#FFF8E0", fg="#8B4513", pady=5)
    pending_title.pack(anchor=tk.CENTER, pady=5)

    pending_separator = ttk.Separator(pending_panel, orient='horizontal')
    pending_separator.pack(fill=X, pady=5)

    pending_content = tk.Frame(pending_panel, bg="#FFF8E0")
    pending_content.pack(fill=BOTH, expand=True, pady=5)

    # Right sidebar with image
    right_sidebar = tk.Frame(content_frame, bg="#FFF8DC", padx=10, pady=10, relief=tk.RIDGE, bd=1)
    right_sidebar.pack(side=RIGHT, fill=Y, padx=10)


    r_img = ImageTk.PhotoImage(Image.open('cashew.jpg'))
    right_img_label = tk.Label(right_sidebar, image=r_img, bg="#FFF8DC", relief=tk.GROOVE, bd=2)
    right_img_label.image = r_img
    right_img_label.pack(pady=10)

    # Get the current date and calculate the previous day's date
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    y = yesterday.strftime('%Y-%m-%d')

    # Populate Last Day Expenses panel
    try:
        # SQL query to fetch expenses for the previous day
        sql = "SELECT * FROM expenses WHERE adate='%s'" % (y)
        print("Executing SQL:", sql)
        cur.execute(sql)
        results = cur.fetchall()
        print("Query Results:", results)

        # Creating a scrollable frame for expenses
        expenses_canvas = tk.Canvas(expenses_content, bg="#FFF8E0", highlightthickness=0)
        expenses_scrollbar = ttk.Scrollbar(expenses_content, orient="vertical", command=expenses_canvas.yview)
        expenses_scrollable_frame = tk.Frame(expenses_canvas, bg="#FFF8E0")

        expenses_scrollable_frame.bind(
            "<Configure>",
            lambda e: expenses_canvas.configure(scrollregion=expenses_canvas.bbox("all"))
        )

        expenses_canvas.create_window((0, 0), window=expenses_scrollable_frame, anchor="nw")
        expenses_canvas.configure(yscrollcommand=expenses_scrollbar.set)

        expenses_canvas.pack(side="left", fill="both", expand=True)
        expenses_scrollbar.pack(side="right", fill="y")
        tk.Label(expenses_scrollable_frame, text="Expense for", font=("Roboto", 11, "bold"),
                 bg="#FFF8E0", fg="#8B4513").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(expenses_scrollable_frame, text="Amount (₹)", font=("Roboto", 11, "bold"),
                 bg="#FFF8E0", fg="#8B4513").grid(row=0, column=1, padx=5, pady=5, sticky="e")
        tk.Frame(expenses_scrollable_frame, height=2, width=320, bg="#8B4513").grid(row=1, column=0, columnspan=2,
                                                                                    pady=5)

        i = 2
        total = 0
        for result in results:
            tk.Label(expenses_scrollable_frame, text=result[2], font=("Roboto", 10),
                     bg="#FFF8E0", fg="#000000").grid(row=i, column=0, padx=5, pady=3, sticky="w")
            tk.Label(expenses_scrollable_frame, text=f"{float(result[3]):.2f}", font=("Roboto", 10),
                     bg="#FFF8E0", fg="#000000").grid(row=i, column=1, padx=5, pady=3, sticky="e")
            i += 1
            total += float(result[3])

        total_rounded = round(total, 2)

        # Adding a separator line before total
        tk.Frame(expenses_scrollable_frame, height=2, width=320, bg="#8B4513").grid(row=i, column=0, columnspan=2,
                                                                                    pady=5)
        i += 1

        # Adding total with professional styling
        tk.Label(expenses_scrollable_frame, text="Total Expenses", font=("Roboto", 12, "bold"),
                 bg="#FFF8E0", fg="#008000").grid(row=i, column=0, padx=5, pady=5, sticky="w")
        tk.Label(expenses_scrollable_frame, text=f"₹ {total_rounded:.2f}", font=("Roboto", 12, "bold"),
                 bg="#FFF8E0", fg="#008000").grid(row=i, column=1, padx=5, pady=5, sticky="e")

    except Exception as e:
        print("Error:", e)
        tk.Label(expenses_content, text="Error fetching data", font=("Roboto", 12),
                 bg="#FFF8E0", fg="#B22222").pack(pady=20)

    # Populating Last Day Sale panel
    try:
        # SQL query to fetch sales for the previous day
        sql = "SELECT * FROM sell WHERE adate='%s'" % (y)
        print("Executing SQL:", sql)
        cur.execute(sql)
        results = cur.fetchall()
        print("Query Results:", results)
        sales_canvas = tk.Canvas(sales_content, bg="#FFF8E0", highlightthickness=0)
        sales_scrollbar = ttk.Scrollbar(sales_content, orient="vertical", command=sales_canvas.yview)
        sales_scrollable_frame = tk.Frame(sales_canvas, bg="#FFF8E0")

        sales_scrollable_frame.bind(
            "<Configure>",
            lambda e: sales_canvas.configure(scrollregion=sales_canvas.bbox("all"))
        )

        sales_canvas.create_window((0, 0), window=sales_scrollable_frame, anchor="nw")
        sales_canvas.configure(yscrollcommand=sales_scrollbar.set)

        sales_canvas.pack(side="left", fill="both", expand=True)
        sales_scrollbar.pack(side="right", fill="y")

        # Creating headers for sales
        tk.Label(sales_scrollable_frame, text="Client", font=("Roboto", 11, "bold"),
                 bg="#FFF8E0", fg="#8B4513").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(sales_scrollable_frame, text="Amount (₹)", font=("Roboto", 11, "bold"),
                 bg="#FFF8E0", fg="#8B4513").grid(row=0, column=1, padx=5, pady=5, sticky="e")

        # Adding a separator line
        tk.Frame(sales_scrollable_frame, height=2, width=320, bg="#8B4513").grid(row=1, column=0, columnspan=2, pady=5)

        i = 2
        total = 0
        for result in results:
            tk.Label(sales_scrollable_frame, text=result[2], font=("Roboto", 10),
                     bg="#FFF8E0", fg="#000000").grid(row=i, column=0, padx=5, pady=3, sticky="w")
            tk.Label(sales_scrollable_frame, text=f"{float(result[6]):.2f}", font=("Roboto", 10),
                     bg="#FFF8E0", fg="#000000").grid(row=i, column=1, padx=5, pady=3, sticky="e")
            i += 1
            total += result[6]

        total_rounded = round(total, 2)

        # Adding a separator line before total
        tk.Frame(sales_scrollable_frame, height=2, width=320, bg="#8B4513").grid(row=i, column=0, columnspan=2, pady=5)
        i += 1

        # Adding total with professional styling
        tk.Label(sales_scrollable_frame, text="Total Sales", font=("Roboto", 12, "bold"),
                 bg="#FFF8E0", fg="#008000").grid(row=i, column=0, padx=5, pady=5, sticky="w")
        tk.Label(sales_scrollable_frame, text=f"₹ {total_rounded:.2f}", font=("Roboto", 12, "bold"),
                 bg="#FFF8E0", fg="#008000").grid(row=i, column=1, padx=5, pady=5, sticky="e")

    except Exception as e:
        print("Error:", e)
        tk.Label(sales_content, text="Error fetching data", font=("Roboto", 12),
                 bg="#FFF8E0", fg="#B22222").pack(pady=20)

    # Populating Payment Pending panel
    try:
        # SQL query to fetch pending payments
        sql = "SELECT * FROM sell WHERE paid='not paid' ORDER BY adate"
        print("Executing SQL:", sql)
        cur.execute(sql)
        results = cur.fetchall()
        print("Query Results:", results)

        # Creating a scrollable frame for pending payments
        pending_canvas = tk.Canvas(pending_content, bg="#FFF8E0", highlightthickness=0)
        pending_scrollbar = ttk.Scrollbar(pending_content, orient="vertical", command=pending_canvas.yview)
        pending_scrollable_frame = tk.Frame(pending_canvas, bg="#FFF8E0")

        pending_scrollable_frame.bind(
            "<Configure>",
            lambda e: pending_canvas.configure(scrollregion=pending_canvas.bbox("all"))
        )

        pending_canvas.create_window((0, 0), window=pending_scrollable_frame, anchor="nw")
        pending_canvas.configure(yscrollcommand=pending_scrollbar.set)

        pending_canvas.pack(side="left", fill="both", expand=True)
        pending_scrollbar.pack(side="right", fill="y")

        # Creating headers for pending payments
        tk.Label(pending_scrollable_frame, text="Date", font=("Roboto", 11, "bold"),
                 bg="#FFF8E0", fg="#8B4513").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(pending_scrollable_frame, text="Client", font=("Roboto", 11, "bold"),
                 bg="#FFF8E0", fg="#8B4513").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Label(pending_scrollable_frame, text="Amount (₹)", font=("Roboto", 11, "bold"),
                 bg="#FFF8E0", fg="#8B4513").grid(row=0, column=2, padx=5, pady=5, sticky="e")

        tk.Frame(pending_scrollable_frame, height=2, width=320, bg="#8B4513").grid(row=1, column=0, columnspan=3,
                                                                                   pady=5)

        i = 2
        total = 0
        for result in results:
            tk.Label(pending_scrollable_frame, text=result[1], font=("Roboto", 10),
                     bg="#FFF8E0", fg="#000000").grid(row=i, column=0, padx=5, pady=3, sticky="w")
            tk.Label(pending_scrollable_frame, text=result[2], font=("Roboto", 10),
                     bg="#FFF8E0", fg="#000000").grid(row=i, column=1, padx=5, pady=3, sticky="w")
            tk.Label(pending_scrollable_frame, text=f"{float(result[6]):.2f}", font=("Roboto", 10),
                     bg="#FFF8E0", fg="#000000").grid(row=i, column=2, padx=5, pady=3, sticky="e")
            i += 1
            total += result[6]

        total_rounded = round(total, 2)

        # a separator line before total
        tk.Frame(pending_scrollable_frame, height=2, width=320, bg="#8B4513").grid(row=i, column=0, columnspan=3,
                                                                                   pady=5)
        i += 1


        tk.Label(pending_scrollable_frame, text="Total Pending", font=("Roboto", 12, "bold"),
                 bg="#FFF8E0", fg="#008000").grid(row=i, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        tk.Label(pending_scrollable_frame, text=f"₹ {total_rounded:.2f}", font=("Roboto", 12, "bold"),
                 bg="#FFF8E0", fg="#008000").grid(row=i, column=2, padx=5, pady=5, sticky="e")

    except Exception as e:
        print("Error:", e)
        tk.Label(pending_content, text="Error fetching data", font=("Roboto", 12),
                 bg="#FFF8E0", fg="#B22222").pack(pady=20)

    # Footer with date and version info
    footer_frame = tk.Frame(main_container, bg="#FFF8DC", pady=5)
    footer_frame.pack(fill=X, side=BOTTOM)

    date_label = tk.Label(footer_frame,
                          text=f"Date: {today.strftime('%d-%m-%Y')}",
                          font=("Roboto", 9),
                          fg="#8B4513",
                          bg="#FFF8DC")
    date_label.pack(side=LEFT, padx=10)

    version_label = tk.Label(footer_frame,
                             text="v1.0.0",
                             font=("Roboto", 9),
                             fg="#8B4513",
                             bg="#FFF8DC")
    version_label.pack(side=RIGHT, padx=10)

    # Adding backup button AFTER all other UI elements are created
    BackupSystem.add_backup_button(application)
    BackupSystem.schedule_automatic_backups()

    application.mainloop()

def _generate_qr_code_background(self):
    """Background task to generate the QR code."""
    try:
        # Running demand_prediction.py to generate the output image
        self.run_demand_prediction()

        # Checking if the output file exists
        output_file_path = os.path.join(os.path.dirname(__file__), "demand_prediction_output.png")
        if not os.path.exists(output_file_path):
            print(f"Error: File '{output_file_path}' not found after running 'demand_prediction.py'.")
            return

        # Uploading the image to Google Drive
        shareable_link = self.upload_image_to_drive(output_file_path)
        if not shareable_link:
            print("Error: Failed to upload image to Google Drive.")
            return

        # Generating QR code with the shareable link
        qr = qrcode.QRCode(
            version=1,  # Starting with version 1 (smallest)
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2,
        )
        qr.add_data(shareable_link)
        qr.make(fit=True)

        # Create an image from the QR code
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code as an image
        qr_image_path = os.path.join(os.path.dirname(__file__), "qr_code.png")
        qr_image.save(qr_image_path)

        # Update the GUI with the QR code and message
        self.root.after(0, self._update_qr_code_gui, qr_image_path)

    except Exception as e:
        print(f"Error generating QR code: {e}")

def run_demand_prediction(self):
    try:
        # Run the demand prediction process
        demand_prediction.show_demand_prediction()
        print("demand_prediction.py executed successfully.")
    except Exception as e:
        print(f"Error running demand_prediction.py: {e}")


def check_db():
    
    try:
        l.execute("CREATE TABLE IF NOT EXISTS user(username varchar(50) not null primary key,password varchar(50) not null,question varchar(50) not null,answer varchar(50) not null);")
        l.execute("CREATE TABLE IF NOT EXISTS 'payment' ('adate' date NOT NULL,'rs' int(11) NOT NULL,'remark' text NOT NULL,'type' text NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'clients' ('id' integer PRIMARY KEY AUTOINCREMENT,'name' text NOT NULL,'address' text NOT NULL,'mobile' int(12) NOT NULL,'phone' int(12) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'expenses'( 'id' integer PRIMARY KEY AUTOINCREMENT,'adate' date NOT NULL, 'name' text NOT NULL,'rs' double NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'ot'( 'adate' date NOT NULL, 'name' text NOT NULL,'hour' int(2) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'labour_payment' ('adate' date NOT NULL,'name' text NOT NULL,'rs' decimal(10,0) NOT NULL,'ot' decimal(10,0) NOT NULL,'total' decimal(10,0) NOT NULL,'shift' int(1) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'labour_attendance' ('name' text NOT NULL,'Jun' text NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'labour_details' ('id' integer PRIMARY KEY AUTOINCREMENT,'name' text NOT NULL,'other' text NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'production' ('adate' date NOT NULL,'tf' int(11) NOT NULL,'fh' int(11) NOT NULL,'ts' int(11) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'production_payas' ('adate' date NOT NULL,'tf' int(11) NOT NULL,'fh' int(11) NOT NULL,'ts' int(11) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'production_oras' ('adate' date NOT NULL,'tf' int(11) NOT NULL,'fh' int(11) NOT NULL,'ts' int(11) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'production_34gram' ('adate' date NOT NULL,'tf' int(11) NOT NULL,'fh' int(11) NOT NULL,'ts' int(11) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'raw_material' ('id' integer PRIMARY KEY AUTOINCREMENT,'adate' date NOT NULL,'raw' text NOT NULL,'type' text NOT NULL,'quantity' int(11) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'raw_material_payas' ('id' integer PRIMARY KEY AUTOINCREMENT,'adate' date NOT NULL,'raw' text NOT NULL,'type' text NOT NULL,'quantity' int(11) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'raw_material_oras' ('id' integer PRIMARY KEY AUTOINCREMENT,'adate' date NOT NULL,'raw' text NOT NULL,'type' text NOT NULL,'quantity' int(11) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'raw_material_34gram' ('id' integer PRIMARY KEY AUTOINCREMENT,'adate' date NOT NULL,'raw' text NOT NULL,'type' text NOT NULL,'quantity' int(11) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'sell' ( 'id' integer PRIMARY KEY AUTOINCREMENT,'adate' date NOT NULL,'client' text NOT NULL,'item' text NOT NULL,'quantity' int(11) NOT NULL,'rate' double NOT NULL,'total' double NOT NULL,'paid' text NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'stock_maintenance'('tf' int(11) NOT NULL,'fh' int(11) NOT NULL,'ts' int(11) NOT NULL, 'preform250' int(11) NOT NULL,'preform500' int(11) NOT NULL,'preform1000' int(11) NOT NULL,'lable250' int(11) NOT NULL,'lable500' int(11) NOT NULL,'lable1000' int(11) NOT NULL,'caps250' int(11) NOT NULL,'caps500' int(11) NOT NULL,'caps1000' int(11) NOT NULL,'boxes250' int(11) NOT NULL,'boxes500' int(11) NOT NULL,'boxes1000' int(11) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'stock_maintenance_payas'('tf' int(11) NOT NULL,'fh' int(11) NOT NULL,'ts' int(11) NOT NULL, 'preform250' int(11) NOT NULL,'preform500' int(11) NOT NULL,'preform1000' int(11) NOT NULL,'lable250' int(11) NOT NULL,'lable500' int(11) NOT NULL,'lable1000' int(11) NOT NULL,'caps250' int(11) NOT NULL,'caps500' int(11) NOT NULL,'caps1000' int(11) NOT NULL,'boxes250' int(11) NOT NULL,'boxes500' int(11) NOT NULL,'boxes1000' int(11) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'stock_maintenance_oras'('tf' int(11) NOT NULL,'fh' int(11) NOT NULL,'ts' int(11) NOT NULL, 'preform250' int(11) NOT NULL,'preform500' int(11) NOT NULL,'preform1000' int(11) NOT NULL,'lable250' int(11) NOT NULL,'lable500' int(11) NOT NULL,'lable1000' int(11) NOT NULL,'caps250' int(11) NOT NULL,'caps500' int(11) NOT NULL,'caps1000' int(11) NOT NULL,'boxes250' int(11) NOT NULL,'boxes500' int(11) NOT NULL,'boxes1000' int(11) NOT NULL)")
        l.execute("CREATE TABLE IF NOT EXISTS 'stock_maintenance_34gram'('tf' int(11) NOT NULL,'fh' int(11) NOT NULL,'ts' int(11) NOT NULL, 'preform250' int(11) NOT NULL,'preform500' int(11) NOT NULL,'preform1000' int(11) NOT NULL,'lable250' int(11) NOT NULL,'lable500' int(11) NOT NULL,'lable1000' int(11) NOT NULL,'caps250' int(11) NOT NULL,'caps500' int(11) NOT NULL,'caps1000' int(11) NOT NULL,'boxes250' int(11) NOT NULL,'boxes500' int(11) NOT NULL,'boxes1000' int(11) NOT NULL)")
        l.execute("select * from stock_maintenance")

        if l.fetchone() is None:
            l.execute("insert into stock_maintenance values(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)")

        l.execute("select * from stock_maintenance_payas")

        if l.fetchone() is None:
            l.execute("insert into stock_maintenance_payas values(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)")

        l.execute("select * from stock_maintenance_oras")

        if l.fetchone() is None:
            l.execute("insert into stock_maintenance_oras values(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)")
            
        l.execute("select * from stock_maintenance_34gram")

        if l.fetchone() is None:
            l.execute("insert into stock_maintenance_34gram values(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)")
            
        login.commit()
        insert_info("Datebase Created Successfully or Already Exist")
        
    except Exception as exp:
        insert_error(exp)	
        
    
    
    
check_db()  
again()