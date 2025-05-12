import pickle
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import mysql.connector
from datetime import date

# Color Scheme for UI
PRIMARY_BG = "#1A2639"  # Dark blue
SECONDARY_BG = "#3E4A61"  # Medium blue
ACCENT_COLOR = "#C24D2C"  # Orange accent
TEXT_COLOR = "#FFFFFF"  # White text
BUTTON_BG = "#3E4A61"  # Button background
HIGHLIGHT_BG = "#C24D2C"  # Highlight color
HEADER_BG = "#3E4A61"  # Header background
CHECKBOX_PRESENT = "#4CAF50"  # Green for present
CHECKBOX_ABSENT = "#F44336"  # Red for absent

# Database connection
c = mysql.connector.connect(host="localhost", user="Admin", password="newpassword123", database="cfms")
cur = c.cursor()

# Global Variables
month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
         'August', 'September', 'October', 'November', 'December']
now = date.today()
current_month = now.month - 1
mo = month[current_month]
labour_names = []
current_focus = (0, 0)  # (row, col) tracking for keyboard navigation


def setup_window(window, title):
    window.title(title)
    window.state("zoomed")
    window.configure(background=PRIMARY_BG)
    return window


def load_pickle():
    global labour_names
    try:
        with open("dict.pickle", "rb") as pickle_read:
            dict_temp = pickle.load(pickle_read)
            total_temp = pickle.load(pickle_read)
    except Exception as exp:
        print("Error loading pickle:", exp)
        dict_temp = {}
        total_temp = {}

    for m in month:
        if m not in dict_temp:
            dict_temp[m] = {}
            total_temp[m] = {}

        for name in labour_names:
            if name not in dict_temp[m]:
                dict_temp[m][name] = [0] * 31
                total_temp[m][name] = 0

    return dict_temp, total_temp


def save_to_db():
    global dict, mo, labour_names, cur, c
    for name in labour_names:
        for day in range(31):
            attendance = dict[mo][name][day]
            sql = """
                INSERT INTO labour_attendance (name, month, day, attendance)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE attendance = %s
            """
            cur.execute(sql, (name, mo, day + 1, attendance, attendance))
    c.commit()

def readstatus(ch_var):
    global dict, total, mo, labour_names

    for name in labour_names:
        a = sum(int(ch_var[mo][name][i].get()) for i in range(31))
        total[mo][name] = a
        for i in range(31):
            dict[mo][name][i] = int(ch_var[mo][name][i].get())

    with open("dict.pickle", "wb") as pickle_out:
        pickle.dump(dict, pickle_out)
        pickle.dump(total, pickle_out)

    save_to_db()
    messagebox.showinfo('Success', 'Attendance Successfully Inserted')
    awindow.destroy()

def change(dict, root):
    return {
        month: {
            name: [tk.IntVar(master=root, value=dict.get(month, {}).get(name, [0]*31)[i])
            for i in range(31)]
            for name in labour_names
        }
        for month in month
    }


def change_month(offset):
    global mo, var, current_focus
    current_index = month.index(mo)
    new_index = (current_index + offset) % 12
    mo = month[new_index]
    current_focus = (0, 0)  # Reset focus on month change
    var = change(dict, window)
    update_ui()
    set_focus(current_focus[0], current_focus[1])


def toggle_attendance(name, day):
    current_val = var[mo][name][day].get()
    var[mo][name][day].set(1 - current_val)
    update_checkbox_appearance(name, day)


def update_checkbox_appearance(name, day):
    row = labour_names.index(name) + 2  # +2 for header rows
    col = day + 1  # +1 for name column
    check_frame = window.grid_slaves(row=row, column=col)[0]
    check_label = check_frame.winfo_children()[0]

    if var[mo][name][day].get() == 1:
        check_label.config(bg=CHECKBOX_PRESENT, fg=TEXT_COLOR, text='✔')
    else:
        check_label.config(bg=CHECKBOX_ABSENT, fg=TEXT_COLOR, text='✘')


def set_focus(row, col):
    global current_focus
    max_row = len(labour_names) + 1  # +1 for header row
    max_col = 31  # Days columns

    # Validate bounds
    row = max(0, min(row, max_row - 1))
    col = max(0, min(col, max_col - 1))

    current_focus = (row, col)

    if row >= 2:  # Attendance rows
        highlight_cell(row, col + 1)  # +1 because names are in column 0


def highlight_cell(row, col):
    # First removing highlight from all cells
    for r in range(2, len(labour_names) + 2):
        for c in range(1, 32):  # 31 days + name column
            try:
                frame = window.grid_slaves(row=r, column=c)[0]
                frame.config(highlightbackground=SECONDARY_BG, highlightthickness=1)
            except IndexError:
                pass

    # Highlighting current cell
    try:
        frame = window.grid_slaves(row=row, column=col)[0]
        frame.config(highlightbackground=ACCENT_COLOR, highlightthickness=3)
        frame.focus_set()
    except IndexError:
        pass


def handle_key_press(event):
    row, col = current_focus

    if event.keysym == 'Up':
        set_focus(row - 1, col)
    elif event.keysym == 'Down':
        set_focus(row + 1, col)
    elif event.keysym == 'Left':
        set_focus(row, col - 1)
    elif event.keysym == 'Right':
        set_focus(row, col + 1)
    elif event.keysym in ('Return', 'space'):
        if row >= 2:  # Attendance rows
            name = labour_names[row - 2]
            day = col
            toggle_attendance(name, day)


def update_ui():
    global window, mo, var, dict, labour_names, canvas

    # Clearing the window
    for widget in window.winfo_children():
        widget.destroy()

    # Month Navigation Frame
    nav_frame = tk.Frame(window, bg=HEADER_BG, padx=20, pady=10)
    nav_frame.grid(row=0, column=0, columnspan=32, sticky="ew")

    # Previous Month Button
    prev_button = tk.Button(nav_frame, text="◀ PREV",
                            command=lambda: change_month(-1),
                            font=("Segoe UI", 12, "bold"),
                            bg=BUTTON_BG, fg=TEXT_COLOR,
                            relief=tk.FLAT)
    prev_button.pack(side=LEFT)

    # Month Title
    month_label = Label(nav_frame, text=f"ATTENDANCE FOR {mo.upper()}",
                        font=("Segoe UI", 16, "bold"),
                        fg=TEXT_COLOR, bg=HEADER_BG)
    month_label.pack(side=LEFT, expand=True, padx=20)

    # Next Month Button
    next_button = tk.Button(nav_frame, text="NEXT ▶",
                            command=lambda: change_month(1),
                            font=("Segoe UI", 12, "bold"),
                            bg=BUTTON_BG, fg=TEXT_COLOR,
                            relief=tk.FLAT)
    next_button.pack(side=RIGHT)

    # Date Headers
    for i in range(1, 32):
        date_label = Label(window, text=str(i),
                           font=("Segoe UI", 10, "bold"),
                           bg=HEADER_BG,
                           fg=TEXT_COLOR,
                           width=4,
                           padx=5,
                           pady=5)
        date_label.grid(row=1, column=i, sticky="ew", padx=1, pady=1)

    # Attendance Grid
    for j, name in enumerate(labour_names, start=2):
        # Name Label
        name_label = Label(window, text=name,
                           font=("Segoe UI", 11),
                           bg=PRIMARY_BG,
                           fg=TEXT_COLOR,
                           anchor='w',
                           padx=10)
        name_label.grid(row=j, column=0, sticky='ew')

        # Check buttons
        for i in range(31):
            check_frame = tk.Frame(window,
                                   bg=PRIMARY_BG,
                                   highlightbackground=SECONDARY_BG,
                                   highlightthickness=1)
            check_frame.grid(row=j, column=i + 1, padx=1, pady=1)

            check_label = Label(check_frame,
                                text='✘',
                                font=('Segoe UI', 10),
                                bg=CHECKBOX_ABSENT,
                                fg=TEXT_COLOR,
                                width=3,
                                height=1)
            check_label.pack(expand=True, fill='both')

            # Setting initial state
            if var[mo][name][i].get() == 1:
                check_label.config(bg=CHECKBOX_PRESENT, text='✔')

            # Bind events
            check_frame.bind("<Button-1>", lambda e, n=name, d=i: toggle_attendance(n, d))
            check_label.bind("<Button-1>", lambda e, n=name, d=i: toggle_attendance(n, d))

            # Bind keyboard focus
            check_frame.bind("<FocusIn>", lambda e, r=j, c=i + 1: highlight_cell(r, c))

    # Button Frame
    # Button Frame - Centered and compact
    button_frame = tk.Frame(window, bg=PRIMARY_BG, pady=20)
    button_frame.grid(row=len(labour_names) + 2, column=0, columnspan=32, sticky="nsew")

    # Using a sub-frame to center the buttons together
    button_container = tk.Frame(button_frame, bg=PRIMARY_BG)
    button_container.pack(expand=True)

    # Update Button
    update_button = tk.Button(button_container, text="SAVE ATTENDANCE",
                              command=lambda: readstatus(var),
                              font=("Segoe UI", 12, "bold"),
                              bg=ACCENT_COLOR,
                              fg=TEXT_COLOR,
                              padx=20,
                              pady=10,
                              width=15)
    update_button.pack(side=LEFT, padx=10)

    # Return Button
    return_button = tk.Button(button_container, text="RETURN TO MAIN MENU",
                              command=awindow.destroy,
                              font=("Segoe UI", 10),
                              bg=BUTTON_BG,
                              fg=TEXT_COLOR,
                              padx=20,
                              pady=10,
                              width=15)
    return_button.pack(side=LEFT, padx=10)

    # Configuring grid weights for proper centering
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_rowconfigure(0, weight=1)

    # Configure grid weights
    for i in range(32):
        window.grid_columnconfigure(i, weight=1 if i == 0 else 0)
    window.grid_rowconfigure(0, weight=0)
    window.grid_rowconfigure(1, weight=0)
    for i in range(2, len(labour_names) + 2):
        window.grid_rowconfigure(i, weight=1)

    # Setting initial focus
    set_focus(2, 0)


def main():
    global dict, mo, labour_names, var, awindow, total, window, canvas

    cur.execute("SELECT name FROM labour_details")
    labour_names = [row[0] for row in cur.fetchall()]

    dict, total = load_pickle()
    awindow = Tk()
    awindow = setup_window(awindow, "Labour Attendance System")

    # Creating main container
    main_frame = tk.Frame(awindow, bg=PRIMARY_BG)
    main_frame.pack(fill=BOTH, expand=True)

    # Creating canvas with scrollbar
    canvas = Canvas(main_frame, bg=PRIMARY_BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    window = tk.Frame(canvas, bg=PRIMARY_BG)
    canvas.create_window((0, 0), window=window, anchor=NW)

    # Binding keyboard events
    awindow.bind("<Up>", handle_key_press)
    awindow.bind("<Down>", handle_key_press)
    awindow.bind("<Left>", handle_key_press)
    awindow.bind("<Right>", handle_key_press)
    awindow.bind("<Return>", handle_key_press)
    awindow.bind("<space>", handle_key_press)

    var = change(dict, window)
    update_ui()

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig('window', width=event.width)

    window.bind("<Configure>", on_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig('window', width=e.width))

    awindow.mainloop()


if __name__ == "__main__":
    main()