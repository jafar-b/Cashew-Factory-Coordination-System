from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox, font
import mysql.connector
from datetime import date

now = date.today()

month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
         'December']

# Database connection
c = mysql.connector.connect(host="localhost", user="Admin", password="newpassword123", database="cfms")
cur = c.cursor()

# Global variables
flag = None
name, rs = [], []

# Color scheme for UI
PRIMARY_BG = "#1A2639"  # Dark blue
SECONDARY_BG = "#3E4A61"  # Medium blue
ACCENT_COLOR = "#C24D2C"  # Orange accent
TEXT_COLOR = "#FFFFFF"  # White text
BUTTON_BG = "#3E4A61"  # Button background
BUTTON_FG = "#FFFFFF"  # Button text
HIGHLIGHT_BG = "#C24D2C"  # Highlight color
HEADER_BG = "#3E4A61"  # Header background
ENTRY_BG = "#F9F8F8"  # Light entry background


def setup_window(window, title):
    """Setting up common window properties"""
    window.title(title)
    window.state("zoomed")
    window.configure(background=PRIMARY_BG)

    # Configuring common styles
    style = Style()
    style.configure('TLabel', background=PRIMARY_BG, foreground=TEXT_COLOR, font=('Segoe UI', 10))
    style.configure('Header.TLabel', background=HEADER_BG, foreground=TEXT_COLOR, font=('Segoe UI', 14, 'bold'))
    style.configure('Title.TLabel', background=HEADER_BG, foreground=TEXT_COLOR, font=('Segoe UI', 16, 'bold'))

    return window


def create_gradient_header(parent, text, row=0, column=0, columnspan=3):
    """Creating a stylish header with gradient-like effect"""
    header_frame = tk.Frame(parent, background=HEADER_BG, padx=20, pady=10)
    header_frame.grid(row=row, column=column, columnspan=columnspan, sticky='ew', pady=10)

    header_label = tk.Label(header_frame, text=text, font=('Segoe UI', 16, 'bold'),
                            background=HEADER_BG, foreground=TEXT_COLOR)
    header_label.pack(padx=20, pady=10)

    return header_frame


def create_styled_button(parent, text, command, row=None, column=None, width=15, is_primary=False):
    """Creating a styled button with hover effect"""
    if is_primary:
        btn = tk.Button(parent, text=text, command=command, width=width,
                        font=('Segoe UI', 11), bg=ACCENT_COLOR, fg=TEXT_COLOR,
                        relief=tk.RAISED, borderwidth=1, padx=10, pady=5)
    else:
        btn = tk.Button(parent, text=text, command=command, width=width,
                        font=('Segoe UI', 11), bg=BUTTON_BG, fg=BUTTON_FG,
                        relief=tk.RAISED, borderwidth=1, padx=10, pady=5)

    # Hover effects
    btn.bind("<Enter>", lambda e: e.widget.config(background=HIGHLIGHT_BG if is_primary else ACCENT_COLOR))
    btn.bind("<Leave>", lambda e: e.widget.config(background=ACCENT_COLOR if is_primary else BUTTON_BG))

    if row is not None and column is not None:
        btn.grid(row=row, column=column, padx=10, pady=10)

    return btn


def create_styled_entry(parent, row, column, width=15):
    """Creating a styled entry field"""
    entry = Entry(parent, font=("Segoe UI", 10), width=width, background=ENTRY_BG)
    entry.grid(row=row, column=column, padx=10, pady=5)
    return entry


def addBox():
    global name, rs, entry_frame

    next_row = len(name)

    name.append(create_styled_entry(entry_frame, next_row + 1, 0))
    rs.append(create_styled_entry(entry_frame, next_row + 1, 2))


def delete_row(id, date=0, month=0):
    success = True
    try:
        sql = "DELETE FROM expenses WHERE id = %s"
        cur.execute(sql, (id,))
        if date != 0:
            ref(date)
        if month != 0:
            get_expenses_for_month(month)
    except Exception as exp:
        c.rollback()
        success = False
        messagebox.showerror("Error", str(exp))
    if success:
        c.commit()
        messagebox.showinfo('Success', 'Expenses Successfully Deleted')


def get_expenses(date, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    # Configure frame grid
    frame.grid_columnconfigure(0, weight=1)

    title_label = tk.Label(frame, text="EXPENSES FOR " + date.strftime("%B %d, %Y"),
                           font=("Segoe UI", 15, "bold"), background=PRIMARY_BG,
                           foreground=TEXT_COLOR)
    title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky='ew')

    # Header frame
    header_frame = tk.Frame(frame, background=HEADER_BG)
    header_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=5)

    # Configure header columns
    header_frame.grid_columnconfigure(0, weight=3, minsize=200)  # Item Name
    header_frame.grid_columnconfigure(1, weight=1, minsize=120)  # Amount
    header_frame.grid_columnconfigure(2, weight=1, minsize=100)  # Action

    tk.Label(header_frame, text="Item Name", font=("Segoe UI", 12, "bold"),
             background=HEADER_BG, foreground=TEXT_COLOR).grid(row=0, column=0, sticky='w', padx=10)
    tk.Label(header_frame, text="Amount (Rs.)", font=("Segoe UI", 12, "bold"),
             background=HEADER_BG, foreground=TEXT_COLOR).grid(row=0, column=1)
    tk.Label(header_frame, text="Action", font=("Segoe UI", 12, "bold"),
             background=HEADER_BG, foreground=TEXT_COLOR).grid(row=0, column=2, padx=10)

    try:
        sql = "SELECT * FROM expenses WHERE adate = %s"
        cur.execute(sql, (date,))
        results = cur.fetchall()

        if not results:
            no_data_label = tk.Label(frame, text="No expenses found for this date.",
                                     font=("Segoe UI", 12, "italic"),
                                     background=PRIMARY_BG, foreground=TEXT_COLOR)
            no_data_label.grid(row=2, column=0, columnspan=3, pady=20)
            return

        # Create a container for expense items
        expense_container = tk.Frame(frame, background=PRIMARY_BG)
        expense_container.grid(row=2, column=0, columnspan=3, sticky='nsew')
        expense_container.grid_columnconfigure(0, weight=1)

        total = 0
        for i, result in enumerate(results):
            # Alternate row colors
            row_bg = SECONDARY_BG if i % 2 == 0 else PRIMARY_BG

            row_frame = tk.Frame(expense_container, background=row_bg)
            row_frame.grid(row=i, column=0, sticky='ew', pady=1)

            # Configure columns to match headers
            row_frame.grid_columnconfigure(0, weight=3, minsize=200)
            row_frame.grid_columnconfigure(1, weight=1, minsize=120)
            row_frame.grid_columnconfigure(2, weight=1, minsize=100)

            tk.Label(row_frame, text=result[2], font=("Segoe UI", 11),
                     background=row_bg, foreground=TEXT_COLOR, anchor='w').grid(
                row=0, column=0, sticky='w', padx=10)

            tk.Label(row_frame, text=f"{float(result[3]):,.2f}", font=("Segoe UI", 11),
                     background=row_bg, foreground=TEXT_COLOR).grid(
                row=0, column=1)

            delete_btn = tk.Button(row_frame, text="Delete", font=("Segoe UI", 10),
                                   command=lambda item=result[0]: delete_row(item, date=date),
                                   bg="#B33A3A", fg="white", width=8)
            delete_btn.grid(row=0, column=2, padx=10)

            # Hover effects
            delete_btn.bind("<Enter>", lambda e: e.widget.config(background="#D32F2F"))
            delete_btn.bind("<Leave>", lambda e: e.widget.config(background="#B33A3A"))

            total += float(result[3])

        # Summary section
        summary_frame = tk.Frame(frame, background=SECONDARY_BG)
        summary_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=10)

        summary_frame.grid_columnconfigure(0, weight=1)
        summary_frame.grid_columnconfigure(1, weight=1)

        tk.Label(summary_frame, text="Total Expenses:", font=("Segoe UI", 12, "bold"),
                 background=SECONDARY_BG, foreground=TEXT_COLOR).grid(
            row=0, column=0, sticky='e', padx=10)

        tk.Label(summary_frame, text=f"Rs. {total:,.2f}", font=("Segoe UI", 12, "bold"),
                 background=SECONDARY_BG, foreground=ACCENT_COLOR).grid(
            row=0, column=1, sticky='w', padx=10)

    except Exception as exp:
        messagebox.showerror("Error", str(exp))


def ref(date):
    global view_frame
    get_expenses(date, view_frame)


def insert_expenses():
    global name, rs, date
    success = True

    # Validate entries
    empty_fields = False
    invalid_amount = False

    for i in range(len(name)):
        if not name[i].get() or not rs[i].get():
            empty_fields = True
            break
        try:
            float(rs[i].get())
        except ValueError:
            invalid_amount = True
            break

    if empty_fields:
        messagebox.showwarning("Validation Error", "Please fill in all fields.")
        return

    if invalid_amount:
        messagebox.showwarning("Validation Error", "Amount must be a valid number.")
        return

    try:
        for i in range(len(name)):
            sql = "INSERT INTO expenses (adate, name, rs) VALUES (%s, %s, %s)"
            values = (date, name[i].get(), float(rs[i].get()))
            cur.execute(sql, values)
    except Exception as exp:
        c.rollback()
        success = False
        messagebox.showerror("Error", str(exp))
    if success:
        c.commit()
        messagebox.showinfo('Success', 'Expenses Successfully Inserted')
        ref(date)


def edit(i):
    global editexp, edit_date, view_frame, date, name, rs, entry_frame

    date = now.replace(day=i)
    name = []
    rs = []
    edit_date.destroy()

    editexp = Tk()
    editexp = setup_window(editexp, f"Edit Expenses - {date.strftime('%B %d, %Y')}")

    # Main container with two sections
    main_container = tk.Frame(editexp, background=PRIMARY_BG)
    main_container.pack(fill=BOTH, expand=True)

    # TOP SECTION - Expense entry components
    top_frame = tk.Frame(main_container, background=PRIMARY_BG)
    top_frame.pack(fill=X, pady=10)

    # Center the entry components horizontally
    center_container = tk.Frame(top_frame, background=PRIMARY_BG)
    center_container.pack(pady=10)

    # Header
    header_label = tk.Label(center_container, text=f"MANAGE EXPENSES - {date.strftime('%B %d, %Y')}",
                            font=("Segoe UI", 18, "bold"),
                            background=PRIMARY_BG, foreground=ACCENT_COLOR)
    header_label.pack(pady=(0, 10))

    # Entry section
    entry_section = tk.Frame(center_container, background=SECONDARY_BG, padx=20, pady=20)
    entry_section.pack()

    # Entry header
    entry_header = tk.Frame(entry_section, background=SECONDARY_BG)
    entry_header.pack(fill=X)

    tk.Label(entry_header, text="Add New Expense", font=("Segoe UI", 14, "bold"),
             background=SECONDARY_BG, foreground=TEXT_COLOR).pack(pady=(0, 10))

    # Entry fields
    entry_frame = tk.Frame(entry_section, background=SECONDARY_BG)
    entry_frame.pack(fill=X, pady=10)

    # Column headers
    tk.Label(entry_frame, text="Item Name", font=("Segoe UI", 12, "bold"),
             background=SECONDARY_BG, foreground=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(entry_frame, text="Amount (Rs.)", font=("Segoe UI", 12, "bold"),
             background=SECONDARY_BG, foreground=TEXT_COLOR).grid(row=0, column=2, padx=10, pady=5)

    # Entry fields
    name.append(create_styled_entry(entry_frame, 1, 0, width=30))
    rs.append(create_styled_entry(entry_frame, 1, 2, width=15))

    # Buttons
    button_frame = tk.Frame(entry_section, background=SECONDARY_BG, pady=10)
    button_frame.pack(fill=X)

    add_box_btn = create_styled_button(button_frame, 'Add Row', addBox)
    add_box_btn.pack(side=LEFT, padx=10)

    insert_btn = create_styled_button(button_frame, 'Save Expenses', insert_expenses, is_primary=True)
    insert_btn.pack(side=LEFT, padx=10)

    back_btn = tk.Button(button_frame, text='Return to Calendar', font=("Segoe UI", 11),
                         command=lambda: go_back_to_editdaylist(editexp),
                         bg=BUTTON_BG, fg=BUTTON_FG, padx=10, pady=5, width=15)
    back_btn.pack(side=RIGHT, padx=10)

    # Get all widgets that should be navigable
    widgets = [
        name[-1],  # Last name entry (most recently added)
        rs[-1],  # Last amount entry
        add_box_btn,
        insert_btn,
        back_btn
    ]

    # Configure keyboard navigation functions
    def focus_next(event):
        current = editexp.focus_get()
        try:
            idx = widgets.index(current)
            next_idx = (idx + 1) % len(widgets)
            widgets[next_idx].focus_set()
        except ValueError:
            widgets[0].focus_set()
        return "break"

    def focus_prev(event):
        current = editexp.focus_get()
        try:
            idx = widgets.index(current)
            next_idx = (idx - 1) % len(widgets)
            widgets[next_idx].focus_set()
        except ValueError:
            widgets[0].focus_set()
        return "break"

    def on_arrow_key(event, direction):
        current = event.widget
        if isinstance(current, tk.Entry):
            info = current.grid_info()
            row, col = info['row'], info['column']

            try:
                if direction == 'up' and row > 1:
                    # Move up to same column in previous row if exists
                    slaves = entry_frame.grid_slaves(row=row - 1, column=col)
                    if slaves:
                        slaves[0].focus_set()
                elif direction == 'down':
                    # Move down to same column in next row if exists
                    slaves = entry_frame.grid_slaves(row=row + 1, column=col)
                    if slaves:
                        slaves[0].focus_set()
                elif direction == 'left' and col > 0:
                    # Move left in same row if exists
                    slaves = entry_frame.grid_slaves(row=row, column=col - 1)
                    if slaves:
                        slaves[0].focus_set()
                elif direction == 'right' and col < 1:
                    # Move right in same row if exists
                    slaves = entry_frame.grid_slaves(row=row, column=col + 1)
                    if slaves:
                        slaves[0].focus_set()
            except IndexError:
                pass  # Ignore if no widget exists in that direction

        return "break"

    # Binding keyboard events to all widgets
    for widget in widgets:
        widget.bind('<Tab>', focus_next)
        widget.bind('<Shift-Tab>', focus_prev)
        widget.bind('<Return>',
                    lambda e: editexp.focus_get().invoke() if hasattr(editexp.focus_get(), 'invoke') else focus_next(e))

        if isinstance(widget, tk.Entry):
            widget.bind('<Up>', lambda e: on_arrow_key(e, 'up'))
            widget.bind('<Down>', lambda e: on_arrow_key(e, 'down'))
            widget.bind('<Left>', lambda e: on_arrow_key(e, 'left'))
            widget.bind('<Right>', lambda e: on_arrow_key(e, 'right'))

    # Set initial focus
    name[-1].focus_set()
    # BOTTOM SECTION - Expense display table (with limited height)
    bottom_frame = tk.Frame(main_container, background=PRIMARY_BG)
    bottom_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

    # Create a container for the expense table
    table_container = tk.Frame(bottom_frame, background=PRIMARY_BG)
    table_container.pack(fill=BOTH, expand=True)

    # Display expenses (without scrollregion)
    view_frame = tk.Frame(table_container, background=PRIMARY_BG)
    view_frame.pack(fill=BOTH, expand=True)

    # Load expenses data
    get_expenses(date, view_frame)

    # Ensuring the window starts with entry section visible
    editexp.update()
    editexp.geometry(
        f"+{int(editexp.winfo_screenwidth() / 2 - editexp.winfo_width() / 2)}+{int(editexp.winfo_screenheight() / 2 - editexp.winfo_height() / 2)}")

    editexp.mainloop()


def go_back_to_editdaylist(current_window):
    current_window.destroy()  # Closing the current edit expenses window
    edit_daylist()  # Reopening the day selection window


def edit_daylist():
    global edit_date, expdate, c, cur, flag, days

    flag = 'edit_date'
    edit_date = Tk()
    edit_date = setup_window(edit_date, 'Edit Expenses - Calendar View')

    # Main container
    main_container = tk.Frame(edit_date, background=PRIMARY_BG)
    main_container.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Header section
    header_frame = tk.Frame(main_container, background=PRIMARY_BG)
    header_frame.pack(fill=X, pady=(0, 20))

    month_label = tk.Label(header_frame, text=f"EXPENSE CALENDAR - {now.strftime('%B %Y')}",
                           font=("Segoe UI", 18, "bold"), background=PRIMARY_BG, foreground=ACCENT_COLOR)
    month_label.pack()

    date_label = tk.Label(header_frame, text=f"Today's Date: {now.strftime('%d %B, %Y')}",
                          font=("Segoe UI", 12, "italic"), background=PRIMARY_BG, foreground=TEXT_COLOR)
    date_label.pack(pady=(5, 0))

    # Calendar container with subtle border effect
    calendar_frame = tk.Frame(main_container, background=SECONDARY_BG, padx=20, pady=20)
    calendar_frame.pack(padx=50, pady=20)

    # Calendar header
    cal_header = tk.Label(calendar_frame, text="Select a Day to Edit Expenses",
                          font=("Segoe UI", 14, "bold"), background=SECONDARY_BG, foreground=TEXT_COLOR)
    cal_header.pack(pady=(0, 20))

    # Calendar grid for days
    button_frame = tk.Frame(calendar_frame, background=SECONDARY_BG)
    button_frame.pack()

    # Day of week headers
    days_of_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for idx, day in enumerate(days_of_week):
        tk.Label(button_frame, text=day, font=("Segoe UI", 11, "bold"),
                 background=SECONDARY_BG, foreground=ACCENT_COLOR).grid(row=0, column=idx, padx=10, pady=5)

    # Calendar buttons
    # Getting the first day of the month (0 = Monday, 6 = Sunday)
    first_day = now.replace(day=1).weekday()
    # Adjusting for Sunday as first column (0 becomes 6, 1 becomes 0, etc.)
    first_day = (first_day + 1) % 7

    # Get the number of days in the current month
    if now.month == 12:
        last_day = now.replace(year=now.year + 1, month=1, day=1)
    else:
        last_day = now.replace(month=now.month + 1, day=1)
    first_of_month = now.replace(day=1)
    days_in_month = (last_day - first_of_month).days

    # Create calendar grid
    day = 1
    row = 1
    col = first_day

    while day <= days_in_month:
        # Highlighting current day
        if day == now.day:
            day_button = tk.Button(button_frame, text=str(day), width=8, height=3,
                                   font=("Segoe UI", 10, "bold"), command=lambda d=day: edit(d),
                                   bg=ACCENT_COLOR, fg="white")
        else:
            day_button = tk.Button(button_frame, text=str(day), width=8, height=3,
                                   font=("Segoe UI", 10), command=lambda d=day: edit(d),
                                   bg=BUTTON_BG, fg=TEXT_COLOR)

        # Hover effects
        day_button.bind("<Enter>", lambda e: e.widget.config(background=HIGHLIGHT_BG))
        day_button.bind("<Leave>", lambda e: e.widget.config(
            background=ACCENT_COLOR if int(e.widget['text']) == now.day else BUTTON_BG))

        day_button.grid(row=row, column=col, padx=4, pady=4)

        # Move to next position
        col += 1
        if col > 6:
            col = 0
            row += 1
        day += 1

    # Back button at bottom
    back_frame = tk.Frame(main_container, background=PRIMARY_BG, pady=10)
    back_frame.pack(side=BOTTOM, fill=X)

    back_button = tk.Button(back_frame, text='Return to Main Menu', font=("Segoe UI", 12),
                            command=edit_date.destroy, width=20, bg=BUTTON_BG, fg=BUTTON_FG)
    back_button.pack(side=RIGHT, padx=20, pady=10)

    edit_date.mainloop()


def get_expenses_for_month(month_number):
    try:
        # Fetching expenses for the specified month
        sql = "SELECT * FROM expenses WHERE MONTH(adate) = %s ORDER BY adate"
        cur.execute(sql, (month_number,))
        results = cur.fetchall()

        # Clear the entry_frame before displaying new data
        for widget in entry_frame.winfo_children():
            widget.destroy()

        if not results:
            no_data_label = tk.Label(entry_frame, text="No expenses found for this month.",
                                     font=("Segoe UI", 14, "italic"), background=PRIMARY_BG, foreground=TEXT_COLOR)
            no_data_label.pack(pady=50)
            return

        # Add month summary header
        month_name = month[month_number - 1]
        summary_header = tk.Label(entry_frame, text=f"EXPENSES SUMMARY - {month_name.upper()}",
                                  font=("Segoe UI", 16, "bold"), background=PRIMARY_BG, foreground=ACCENT_COLOR)
        summary_header.pack(fill=X, pady=(0, 20))

        # Group expenses by date
        expenses_by_date = {}
        total_month = 0

        for result in results:
            expense_date = result[1]  # adate column
            date_str = expense_date.strftime("%d %B, %Y")

            if date_str not in expenses_by_date:
                expenses_by_date[date_str] = []

            expenses_by_date[date_str].append(result)
            total_month += float(result[3])  # Add to total

        # Create a container for all expense groups
        all_expenses_container = tk.Frame(entry_frame, background=PRIMARY_BG)
        all_expenses_container.pack(fill=BOTH, expand=True)

        # Display expenses grouped by date
        for date_str, expenses in expenses_by_date.items():
            # Date header frame
            date_frame = tk.Frame(all_expenses_container, background=HEADER_BG, padx=10, pady=10)
            date_frame.pack(fill=X, pady=(15, 0))

            date_label = tk.Label(date_frame, text=date_str, font=("Segoe UI", 14, "bold"),
                                  background=HEADER_BG, foreground=TEXT_COLOR)
            date_label.pack(side=LEFT, padx=10)

            # Calculating date total
            date_total = sum(float(exp[3]) for exp in expenses)
            total_label = tk.Label(date_frame, text=f"Total: Rs. {date_total:,.2f}",
                                   font=("Segoe UI", 12), background=HEADER_BG, foreground=TEXT_COLOR)
            total_label.pack(side=RIGHT, padx=10)

            # Expenses table for this date
            expenses_table = tk.Frame(all_expenses_container, background=SECONDARY_BG, padx=10, pady=10)
            expenses_table.pack(fill=X)

            # Table headers
            header_frame = tk.Frame(expenses_table, background=SECONDARY_BG)
            header_frame.pack(fill=X)

            # Configure column weights
            header_frame.grid_columnconfigure(0, weight=1, minsize=200)  # Item Name
            header_frame.grid_columnconfigure(1, weight=1, minsize=120)  # Amount
            header_frame.grid_columnconfigure(2, weight=1, minsize=100)  # Action

            tk.Label(header_frame, text="Item Name", width=30, anchor="w", font=("Segoe UI", 12, "bold"),
                     background=SECONDARY_BG, foreground=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=5)
            tk.Label(header_frame, text="Amount (Rs.)", width=15, anchor="w", font=("Segoe UI", 12, "bold"),
                     background=SECONDARY_BG, foreground=TEXT_COLOR).grid(row=0, column=1, padx=10, pady=5)
            tk.Label(header_frame, text="Action", width=10, anchor="w", font=("Segoe UI", 12, "bold"),
                     background=SECONDARY_BG, foreground=TEXT_COLOR).grid(row=0, column=2, padx=10, pady=5)

            # Table rows
            for i, expense in enumerate(expenses):
                row_bg = PRIMARY_BG if i % 2 == 0 else SECONDARY_BG

                row_frame = tk.Frame(expenses_table, background=row_bg)
                row_frame.pack(fill=X)

                # Configure row frame columns
                row_frame.grid_columnconfigure(0, weight=1, minsize=200)
                row_frame.grid_columnconfigure(1, weight=1, minsize=120)
                row_frame.grid_columnconfigure(2, weight=1, minsize=100)

                tk.Label(row_frame, text=expense[2], width=30, anchor="w", font=("Segoe UI", 11),
                         background=row_bg, foreground=TEXT_COLOR).grid(row=0, column=0, sticky='w', padx=10, pady=5)
                tk.Label(row_frame, text=f"{float(expense[3]):,.2f}", width=15, anchor="w", font=("Segoe UI", 11),
                         background=row_bg, foreground=TEXT_COLOR).grid(row=0, column=1, padx=10, pady=5)
                delete_btn = tk.Button(row_frame, text="Delete", width=8, font=("Segoe UI", 10),
                                       command=lambda id=expense[0]: delete_row(id, month=month_number),
                                       bg="#B33A3A", fg=TEXT_COLOR)
                delete_btn.grid(row=0, column=2, padx=10, pady=5)

                # Hover effect for delete button
                delete_btn.bind("<Enter>", lambda e: e.widget.config(background="#D32F2F"))
                delete_btn.bind("<Leave>", lambda e: e.widget.config(background="#B33A3A"))

        # Adding a final summary box
        summary_frame = tk.Frame(all_expenses_container, background=ACCENT_COLOR, padx=20, pady=15)
        summary_frame.pack(fill=X, pady=(20, 5))

        tk.Label(summary_frame, text=f"TOTAL EXPENSES FOR {month_name.upper()}",
                 font=("Segoe UI", 14, "bold"), background=ACCENT_COLOR, foreground="white").pack(side=LEFT, padx=10)

        tk.Label(summary_frame, text=f"Rs. {total_month:,.2f}",
                 font=("Segoe UI", 14, "bold"), background=ACCENT_COLOR, foreground="white").pack(side=RIGHT, padx=10)

    except Exception as exp:
        messagebox.showerror("Error", str(exp))


def view(i):
    global viewdate, name, rs, entry_frame, viewexp
    viewdate.destroy()  # Destroy the month selection window
    viewexp = tk.Tk()
    viewexp = setup_window(viewexp, f'Monthly Expenses - {month[i]}')

    flag = 'viewexp'

    # Main container with visual improvements
    main_container = tk.Frame(viewexp, background=PRIMARY_BG)
    main_container.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Header with more professional styling
    header_frame = tk.Frame(main_container, background=PRIMARY_BG)
    header_frame.pack(fill=X, pady=(0, 20))

    month_title = tk.Label(header_frame, text=f"EXPENSES REPORT",
                           font=("Segoe UI", 18, "bold"), background=PRIMARY_BG, foreground=ACCENT_COLOR)
    month_title.pack(pady=(0, 5))

    # Create a scrollable container for the monthly expense report
    scroll_container = tk.Frame(main_container, background=PRIMARY_BG)
    scroll_container.pack(fill=BOTH, expand=True)

    # Create Canvas with scrollbar for smooth scrolling
    canvas = Canvas(scroll_container, background=PRIMARY_BG, highlightthickness=0)
    scrollbar = Scrollbar(scroll_container, orient="vertical", command=canvas.yview)

    # Configure the scrolling behavior
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Create a frame inside the canvas
    entry_frame = tk.Frame(canvas, background=PRIMARY_BG)
    canvas_window = canvas.create_window((0, 0), window=entry_frame, anchor="nw", tags="entry_frame")

    # Update scroll region when the size changes
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    entry_frame.bind("<Configure>", configure_scroll_region)

    # Make the canvas window width match the canvas width
    def configure_canvas_window(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", configure_canvas_window)

    # Load expenses for the month
    get_expenses_for_month(i + 1)

    # Footer with back button
    footer_frame = tk.Frame(main_container, background=PRIMARY_BG, pady=15)
    footer_frame.pack(side=BOTTOM, fill=X)

    back_button = tk.Button(footer_frame, text='Return to Month Selection', font=("Segoe UI", 12),
                            width=25, command=lambda: go_back_to_viewdaylist(viewexp),
                            bg=BUTTON_BG, fg=BUTTON_FG)
    back_button.pack(side=RIGHT, padx=20)

    viewexp.mainloop()


def go_back_to_viewdaylist(current_window):
    current_window.destroy()  # Close the current monthly expenses window
    view_daylist()  # Reopen the month selection window


def view_daylist():
    global viewdate, expdate, c, cur, flag, days

    viewdate = Tk()
    viewdate = setup_window(viewdate, 'View Monthly Expenses')

    # Main container
    main_container = tk.Frame(viewdate, background=PRIMARY_BG)
    main_container.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Header section
    header_frame = tk.Frame(main_container, background=PRIMARY_BG)
    header_frame.pack(fill=X, pady=(0, 20))

    # Current month display
    month_label = tk.Label(header_frame, text=f"EXPENSE MONTHS",
                           font=("Segoe UI", 18, "bold"), background=PRIMARY_BG, foreground=ACCENT_COLOR)
    month_label.pack()

    # Current date display
    date_label = tk.Label(header_frame, text=f"Today's Date: {now.strftime('%d %B, %Y')}",
                          font=("Segoe UI", 12, "italic"), background=PRIMARY_BG, foreground=TEXT_COLOR)
    date_label.pack(pady=(5, 0))

    # Separator line
    separator = tk.Frame(header_frame, height=2, bg=ACCENT_COLOR)
    separator.pack(fill=X, pady=10)

    # Month selection section
    selection_frame = tk.Frame(main_container, background=PRIMARY_BG)
    selection_frame.pack(pady=20)

    # Instruction label
    instruction_label = tk.Label(selection_frame, text="Select a Month to View Expenses",
                                 font=("Segoe UI", 14, "bold"), background=PRIMARY_BG, foreground=TEXT_COLOR)
    instruction_label.pack(pady=(0, 20))

    # Month buttons grid
    button_frame = tk.Frame(selection_frame, background=PRIMARY_BG)
    button_frame.pack()

    # Arrange months in a 2x6 grid
    for i in range(2):
        for j in range(6):
            month_index = i * 6 + j
            if month_index < 12:
                month_btn = create_styled_button(button_frame, month[month_index],
                                                 lambda idx=month_index: view(idx),
                                                 row=i, column=j, width=15)
                # Special styling for current month
                if month_index == now.month - 1:
                    month_btn.config(bg=ACCENT_COLOR, fg=TEXT_COLOR, font=('Segoe UI', 11, 'bold'))

    # Footer with back button
    footer_frame = tk.Frame(main_container, background=PRIMARY_BG, pady=15)
    footer_frame.pack(side=BOTTOM, fill=X)

    back_button = create_styled_button(footer_frame, 'Return to Main Menu', viewdate.destroy,
                                       is_primary=True, width=20)
    back_button.pack(side=RIGHT, padx=20)

    viewdate.mainloop()


def main_menu():
    global c, cur

    root = Tk()
    root = setup_window(root, "Cashew Factory Management System")

    # Main container
    main_container = tk.Frame(root, background=PRIMARY_BG)
    main_container.pack(fill=BOTH, expand=True, padx=50, pady=50)

    # Header section
    header_frame = tk.Frame(main_container, background=PRIMARY_BG)
    header_frame.pack(fill=X, pady=(0, 50))

    # Application title
    title_label = tk.Label(header_frame, text="CASHEW FACTORY MANAGEMENT SYSTEM",
                           font=("Segoe UI", 24, "bold"),
                           background=PRIMARY_BG, foreground=ACCENT_COLOR)
    title_label.pack()

    # Current date
    date_label = tk.Label(header_frame, text=f"Today: {now.strftime('%A, %d %B %Y')}",
                          font=("Segoe UI", 12), background=PRIMARY_BG, foreground=TEXT_COLOR)
    date_label.pack(pady=(10, 0))

    # Button section
    button_frame = tk.Frame(main_container, background=PRIMARY_BG)
    button_frame.pack(pady=20)

    # Main menu buttons
    edit_btn = create_styled_button(button_frame, "Add/Edit Expenses", edit_daylist,
                                    row=0, column=0, width=25, is_primary=True)
    edit_btn.config(font=('Segoe UI', 12), pady=10)

    view_btn = create_styled_button(button_frame, "View Expenses", view_daylist,
                                    row=1, column=0, width=25, is_primary=True)
    view_btn.config(font=('Segoe UI', 12), pady=10)

    exit_btn = create_styled_button(button_frame, "Exit Application", root.quit,row=2, column=0, width=25)
    exit_btn.config(font=('Segoe UI', 12), pady=10)

    # Footer
    footer_frame = tk.Frame(main_container, background=PRIMARY_BG)
    footer_frame.pack(side=BOTTOM, fill=X, pady=(50, 0))

    # Version/copyright info
    version_label = tk.Label(footer_frame, text="CFMS v1.0 © 2023",
                             font=("Segoe UI", 10),
                             background=PRIMARY_BG, foreground=TEXT_COLOR)
    version_label.pack(side=RIGHT)

    root.mainloop()

if __name__ == "__main__":
    main_menu()


