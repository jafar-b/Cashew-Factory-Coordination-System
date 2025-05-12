from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import pickle
import mysql.connector
from tkinter import messagebox, ttk
from datetime import date
from sqlite3 import dbapi2 as sqlite
from log_maker import *
from datetime import date as dat

# Setting color scheme for UI
BG_COLOR = "#1e1e2f"  # Dark blue-purple background
FG_COLOR = "#ffffff"  # White text
ACCENT_COLOR = "#4e73df"  # Blue accent
DANGER_COLOR = "#e74a3b"  # Red for delete buttons
SUCCESS_COLOR = "#1cc88a"  # Green for success actions
HEADER_COLOR = "#252b3b"  # Darker header color
ENTRY_BG = "#2e3451"  # Dark entry fields
ENTRY_FG = "#ffffff"  # White text for entries
TABLE_HEADER_BG = "#252b3b"  # Table header background
TABLE_HEADER_FG = "#ffffff"  # Table header text
TABLE_ROW_BG1 = "#2e3451"  # Table row background (even)
TABLE_ROW_BG2 = "#353c5a"  # Table row background (odd)
BUTTON_BG_CALCULATE = "#4e73df"  # Calculate button
BUTTON_BG_SUBMIT = "#1cc88a"  # Submit button
BUTTON_BG_RETURN = "#e74a3b"  # Return button
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_NORMAL = ("Segoe UI", 12)
FONT_SMALL = ("Segoe UI", 10)

now = dat.today()

month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
         'December']
aaa = date.today()

cmonth = month[aaa.month - 1]

c = mysql.connector.connect(host="localhost", user="Admin", password="newpassword123", database="cfms")
cur = c.cursor()


def fetch_ot_hours(name):
    """Fetch OT hours for the selected labour from the `ot` table."""
    try:
        sql = "SELECT SUM(hour) FROM ot WHERE name = %s"
        cur.execute(sql, (name,))
        result = cur.fetchone()
        return result[0] if result[0] else 0  # Return 0 if no OT hours are found
    except Exception as exp:
        print(f"Error fetching OT hours: {exp}")
        insert_error(exp)
        return 0


def fetch_attendance_days(name, month):
    """
    Fetch the total number of days a labour has worked from the `labour_attendance` table for the current month.
    """
    try:
        sql = """
            SELECT COUNT(*) 
            FROM labour_attendance 
            WHERE name = %s AND month = %s AND attendance = 1
        """
        cur.execute(sql, (name, month))
        result = cur.fetchone()
        print(f"Attendance days for {name} in {month}: {result[0]}")  # Debugging: Print the result
        return result[0] if result[0] else 0  # Return 0 if no attendance is found
    except Exception as exp:
        print(f"Error fetching attendance days: {exp}")
        insert_error(exp)
        return 0


def insert_payment():
    global date, name, rate, ot, total, shift
    success = True
    try:
        print('pas')

        # Calling the new save_db function to handle insertion into DB
        save_db(date.get(), name.get(), rate.get(), ot.get(), total.get(), shift.get())

        # Updating the dropdown menu with the latest labour names
        update_name_dropdown()

        # Explicitly refreshing the payment details table
        show_payment_details()

        # Clear entry fields or reset them to defaults after submission
        days.set(0)
        ot.set(0)
        rate.set(0.0)
        total.set(0.0)
        shift.set("Day")  # Reset to default shift

    except Exception as exp:
        success = False
        insert_error(exp)

def load_pickle():
    global total_temp
    total_temp = {}
    try:
        pickle_read = open("dict.pickle", "rb")
        dict_temp = pickle.load(pickle_read)
        total_temp = pickle.load(pickle_read)
        pickle_read.close()
    except Exception as exp:
        print(exp)
        insert_error(exp)
    print(total_temp)

    # Ensure total_temp has entries for all labours in the current month
    sql = "SELECT name FROM labour_details"
    cur.execute(sql)
    labour_names = [result[0] for result in cur]

    for labour in labour_names:
        if labour not in total_temp.get(cmonth, {}):
            if cmonth not in total_temp:
                total_temp[cmonth] = {}
            total_temp[cmonth][labour] = 0  # Initialize with 0 if not present


def calculate():
    global days, ot, rate, total
    total.set((days.get() * rate.get()) + (round((ot.get() / 10) * rate.get(), 2)))


def save_pickle():
    """Save the total_temp dictionary to the pickle file."""
    try:
        with open("dict.pickle", "wb") as pickle_file:
            pickle.dump(total_temp, pickle_file)
        print("total_temp saved to dict.pickle")
    except Exception as exp:
        print(f"Error saving total_temp: {exp}")
        insert_error(exp)


def save_db(date_val, name_val, rate_val, ot_val, total_val, shift_val):
    """Function to insert the payment details into the database."""
    try:
        # Construct the SQL query to insert data
        sql = "INSERT INTO labour_payment (adate, name, rs, ot, total, shift) VALUES (DATE('%s'), '%s', %i, %i, %i, '%s')" % (
            date_val, name_val, rate_val, ot_val, total_val, shift_val)
        print("SQL Query:", sql)

        # Execute the SQL query
        cur.execute(sql)

        # Updating total_temp with the new payment
        if cmonth not in total_temp:
            total_temp[cmonth] = {}
        total_temp[cmonth][name_val] = total_temp[cmonth].get(name_val, 0) + total_val

        # Committing changes to the database
        c.commit()
        print("Data inserted successfully into labour_payment table.")

        # Saving updated total_temp to pickle file
        save_pickle()

        # Show success message
        insert_info("Labour Payment Successfully Inserted")
        messagebox.showinfo('Success', 'Labour Payment Successfully Inserted')

        # Refresh the payment details table
        show_payment_details()

    except Exception as exp:
        # Rollback the transaction in case of error
        c.rollback()
        insert_error(exp)
        print("Error inserting into database:", exp)


def update_values(*args):
    global name, days, ot, cmonth, total_temp, now
    selected_name = name.get()

    # Debugging: Print the current month and selected labour
    print(f"Current month: {cmonth}")
    print(f"Selected labour: {selected_name}")

    # Clearing total_temp for the current month to avoid outdated values
    if cmonth in total_temp and selected_name in total_temp[cmonth]:
        total_temp[cmonth][selected_name] = 0

    # Fetch OT hours for the selected labour
    ot_hours = fetch_ot_hours(selected_name)
    ot.set(ot_hours)  # Populate the OT field

    # Fetch attendance days for the selected labour (only for the current month)
    attendance_days = fetch_attendance_days(selected_name, cmonth)
    print(f"Setting days to {attendance_days} for {selected_name}")  # Debugging: Print the days value
    days.set(attendance_days)  # Populate the Days field

    # Set days from total_temp (handling KeyError if labour is not found)
    try:
        total_temp_days = total_temp[cmonth][selected_name]
        days.set(total_temp_days + attendance_days)  # Add total_temp days and attendance days
    except KeyError:
        days.set(attendance_days)  # Default to attendance days if the labour is not found in total_temp
        print(f"Labour '{selected_name}' not found in total_temp for the month '{cmonth}'.")


gui_elements = []
row_positions = {}


def show_payment_details(event=None):
    """Fetch and displaying the payment data in a table format using canvas and scrollbar."""
    global y_position, gui_elements

    # Clear the canvas and reset the GUI elements list
    canvas.delete("all")
    gui_elements.clear()

    # Reset y_position to the starting position
    y_position = 20

    # Get the width of the canvas
    canvas_width = canvas.winfo_width()

    # Print canvas width for debugging
    print(f"Canvas Width: {canvas_width}")

    # Define column widths as a percentage of the canvas width
    column_widths = [0.15, 0.25, 0.15, 0.15, 0.15, 0.15]
    padding = 10  # Adding padding between columns

    # Calculating column positions
    column_positions = []
    current_x = padding  # Start with some padding
    for width in column_widths:
        column_positions.append(current_x)
        current_x += int(canvas_width * width) + padding  # Add padding between columns

    # Create a header background
    header_bg = canvas.create_rectangle(0, 0, canvas_width, y_position + 30, fill=TABLE_HEADER_BG, outline="")

    # Display table headers (column names)
    canvas.create_text(column_positions[0], y_position, anchor="nw", text="Date", font=FONT_HEADER,
                       fill=TABLE_HEADER_FG)
    canvas.create_text(column_positions[1], y_position, anchor="nw", text="Name", font=FONT_HEADER,
                       fill=TABLE_HEADER_FG)
    canvas.create_text(column_positions[2], y_position, anchor="nw", text="Rate", font=FONT_HEADER,
                       fill=TABLE_HEADER_FG)
    canvas.create_text(column_positions[3], y_position, anchor="nw", text="Shift", font=FONT_HEADER,
                       fill=TABLE_HEADER_FG)
    canvas.create_text(column_positions[4], y_position, anchor="nw", text="Total", font=FONT_HEADER,
                       fill=TABLE_HEADER_FG)
    canvas.create_text(column_positions[5], y_position, anchor="nw", text="Action", font=FONT_HEADER,
                       fill=TABLE_HEADER_FG)
    y_position += 40  # Space between headers and rows

    try:
        # Fetch and display existing data from the `labour_payment` table
        sql = "SELECT * FROM labour_payment"
        cur.execute(sql)
        rows = cur.fetchall()

        # Display each row of data
        for i, row in enumerate(rows):
            record_id = (row[0], row[1], row[4])  # an unique identifier for the record

            # Alternate row background colors
            row_bg = TABLE_ROW_BG1 if i % 2 == 0 else TABLE_ROW_BG2
            row_height = 30

            # Creating row background
            canvas.create_rectangle(0, y_position - 5, canvas_width, y_position + row_height,
                                    fill=row_bg, outline="")

            # Creating text for the record
            canvas.create_text(column_positions[0], y_position, anchor="nw", text=row[0], font=FONT_NORMAL,
                               fill=FG_COLOR)
            canvas.create_text(column_positions[1], y_position, anchor="nw", text=row[1], font=FONT_NORMAL,
                               fill=FG_COLOR)
            canvas.create_text(column_positions[2], y_position, anchor="nw", text=row[2], font=FONT_NORMAL,
                               fill=FG_COLOR)
            canvas.create_text(column_positions[3], y_position, anchor="nw", text=row[5], font=FONT_NORMAL,
                               fill=FG_COLOR)
            canvas.create_text(column_positions[4], y_position, anchor="nw", text=row[4], font=FONT_NORMAL,
                               fill=FG_COLOR)

            # Creating a Delete button for the record
            delete_button = tk.Button(canvas, text="Delete", font=FONT_SMALL,
                                      bg=DANGER_COLOR, fg="white",
                                      command=lambda r=record_id: delete_payment_record(r))
            canvas.create_window(column_positions[5], y_position, anchor="nw", window=delete_button)

            y_position += row_height + 10  # Space between rows

        # Update scrollregion to encompass all content
        canvas.config(scrollregion=canvas.bbox("all"))
    except Exception as exp:
        print(f"Error fetching data: {exp}")
        insert_error(exp)


def delete_payment_record(record_id):
    """Delete a record from the `labour_payment` table based on the record ID."""
    try:
        sql = "DELETE FROM labour_payment WHERE adate = %s AND name = %s AND total = %s"
        cur.execute(sql, record_id)
        c.commit()
        insert_info(f"Payment Record Deleted: {record_id}")
        messagebox.showinfo('Success', 'Payment Record Deleted Successfully')

        # Refresh the GUI to reflect the changes
        show_payment_details()

    except Exception as exp:
        c.rollback()
        insert_error(exp)
        messagebox.showerror('Error', 'Failed to Delete Payment Record')


def fetch_labour_names():
    """Fetch the latest list of labour names from the database."""
    try:
        sql = "SELECT name FROM labour_details"
        cur.execute(sql)
        return [row[0] for row in cur.fetchall()]
    except Exception as exp:
        print(f"Error fetching labour names: {exp}")
        insert_error(exp)
        return []


def update_name_dropdown():
    """Update the dropdown menu with the latest list of labour names."""
    global name_option, name_choices

    # Fetch the latest list of labour names
    name_choices = fetch_labour_names()

    # Clear existing options in the dropdown menu
    name_option['menu'].delete(0, 'end')

    # Adding the updated list of labour names to the dropdown menu
    for choice in name_choices:
        name_option['menu'].add_command(label=choice, command=lambda value=choice: name.set(value))


def center_window(window, width, height):
    """Center a tkinter window on the screen."""
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set window size and position
    window.geometry(f"{width}x{height}+{x}+{y}")


def create_styled_button(parent, text, command, bg_color, width=15):
    """Creating a styled button with hover effects."""
    button = tk.Button(
        parent,
        text=text,
        font=FONT_HEADER,
        bg=bg_color,
        fg="white",
        relief="flat",
        borderwidth=0,
        padx=15,
        pady=8,
        width=width,
        command=command
    )

    # Hover effects (darken on hover)
    def on_enter(e):
        button['bg'] = darken_color(bg_color)

    def on_leave(e):
        button['bg'] = bg_color

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    return button


def darken_color(hex_color):
    """Darken a hex color by 20%."""
    # Converting hex to RGB
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)

    # Darken by multiplying by 0.8
    r = int(r * 0.8)
    g = int(g * 0.8)
    b = int(b * 0.8)

    # Convert back to hex
    return f"#{r:02x}{g:02x}{b:02x}"


def create_styled_entry(parent, textvariable, width=20, field_type=None):
    """Creating a styled entry widget with different styling based on field type."""
    # Use white background for specific fields
    if field_type in ["name", "total", "rate"]:
        bg_color = "#ffffff"  # White background
        fg_color = "#000000"  # Black text
    else:
        bg_color = ENTRY_BG  # Dark background
        fg_color = ENTRY_FG  # White text

    # Create the entry with appropriate styling
    entry = tk.Entry(
        parent,
        textvariable=textvariable,
        font=FONT_NORMAL,
        width=width,
        bg=bg_color,
        fg=fg_color,
        insertbackground=fg_color  # Match cursor color to text color
    )
    return entry


def create_styled_label(parent, text, column, row, font=FONT_HEADER):
    """Creating a styled label widget."""
    label = tk.Label(
        parent,
        text=text,
        font=font,
        bg=BG_COLOR,
        fg=FG_COLOR
    )
    label.grid(row=row, column=column, padx=10, pady=10, sticky="e")
    return label


def main():
    global make_payment, now, expdate, flag, entry_frame, date, name, days, ot, rate, total, canvas, y_position, shift, name_option, name_choices
    total = 0.0
    load_pickle()  # Load total_temp from the pickle file
    flag = 'make_payment'
    i = 0

    # Create main window
    make_payment = tk.Tk()
    make_payment.title('Labour Salary Management System')
    make_payment.state("zoomed")
    make_payment.configure(bg=BG_COLOR)

    # Creating a custom style for widgets
    style = ttk.Style()
    style.configure("TFrame", background=BG_COLOR)
    style.configure("TButton", background=ACCENT_COLOR, foreground="white", font=FONT_NORMAL)
    style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=FONT_NORMAL)
    style.configure("TOptionMenu", background=ENTRY_BG, foreground=ENTRY_FG, font=FONT_NORMAL)
    style.configure("TEntry", background=ENTRY_BG, foreground=ENTRY_FG, font=FONT_NORMAL)

    # Header frame
    header_frame = tk.Frame(make_payment, bg=HEADER_COLOR)
    header_frame.pack(fill="x", padx=0, pady=0)

    # App title
    title_label = tk.Label(
        header_frame,
        text="LABOUR SALARY MANAGEMENT SYSTEM",
        font=FONT_TITLE,
        bg=HEADER_COLOR,
        fg=FG_COLOR,
        padx=20,
        pady=15
    )
    title_label.pack(side="left")

    # Current date display
    date_label = tk.Label(
        header_frame,
        text=f"Today: {now}",
        font=FONT_NORMAL,
        bg=HEADER_COLOR,
        fg=FG_COLOR,
        padx=20
    )
    date_label.pack(side="right", padx=20)

    # Main container
    main_container = tk.Frame(make_payment, bg=BG_COLOR)
    main_container.pack(expand=True, fill="both", padx=40, pady=20)

    # Form section
    form_section = tk.Frame(main_container, bg=BG_COLOR)
    form_section.pack(fill="x", pady=20)

    # Form title
    form_title = tk.Label(
        form_section,
        text="New Entry",
        font=FONT_HEADER,
        bg=BG_COLOR,
        fg=ACCENT_COLOR
    )
    form_title.pack(pady=(0, 20))

    # Form frame for inputs
    form_frame = tk.Frame(form_section, bg=BG_COLOR)
    form_frame.pack()

    # Defining variables
    date = StringVar(make_payment, value=aaa)
    name = StringVar(make_payment)
    days = IntVar(make_payment)
    ot = IntVar(make_payment)
    rate = DoubleVar(make_payment)
    total = DoubleVar(make_payment)
    shift = StringVar(make_payment, value="Day")  # Default shift is "Day"

    # Creating form fields
    create_styled_label(form_frame, "Date:", 0, 0)
    create_styled_label(form_frame, "Name:", 0, 1)
    create_styled_label(form_frame, "Days:", 0, 2)
    create_styled_label(form_frame, "OT:", 0, 3)
    create_styled_label(form_frame, "Rate:", 0, 4)
    create_styled_label(form_frame, "Total:", 0, 5)
    create_styled_label(form_frame, "Shift:", 0, 6)

    # Date entry
    date_entry = create_styled_entry(form_frame, date, field_type="date")
    date_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Name dropdown
    name_choices = fetch_labour_names()
    name_option = ttk.Combobox(
        form_frame,
        textvariable=name,
        values=name_choices,
        width=18,
        font=FONT_NORMAL
    )
    # Configure combobox style for white background
    style.configure("TCombobox",
                    fieldbackground="#ffffff",
                    background="#ffffff",
                    foreground="#000000")

    if name_choices:
        name.set(name_choices[0])
    name_option.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    name.trace('w', update_values)

    # Other entries
    days_entry = create_styled_entry(form_frame, days, field_type="days")
    days_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    ot_entry = create_styled_entry(form_frame, ot, field_type="ot")
    ot_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    rate_entry = create_styled_entry(form_frame, rate, field_type="rate")
    rate_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    total_entry = create_styled_entry(form_frame, total, field_type="total")
    total_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

    # Shift dropdown
    shift_choices = ["Day", "Night"]
    shift_option = ttk.Combobox(
        form_frame,
        textvariable=shift,
        values=shift_choices,
        width=18,
        font=FONT_NORMAL
    )
    shift_option.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    # Buttons section
    button_section = tk.Frame(main_container, bg=BG_COLOR)
    button_section.pack(pady=10)

    # Creating buttons
    calculate_button = create_styled_button(
        button_section,
        "Calculate",
        calculate,
        BUTTON_BG_CALCULATE,
        width=10
    )
    calculate_button.grid(row=0, column=0, padx=15)

    submit_button = create_styled_button(
        button_section,
        "Submit",
        insert_payment,
        BUTTON_BG_SUBMIT,
        width=10
    )
    submit_button.grid(row=0, column=1, padx=15)

    return_button = create_styled_button(
        button_section,
        "Return to Main Menu",
        make_payment.destroy,
        BUTTON_BG_RETURN,
        width=20
    )
    return_button.grid(row=0, column=2, padx=15)

    # Records section title
    records_title = tk.Label(
        main_container,
        text="PAYMENT RECORDS",
        font=FONT_HEADER,
        bg=BG_COLOR,
        fg=ACCENT_COLOR
    )
    records_title.pack(pady=(30, 10))

    # Table section with canvas and scrollbar
    table_frame = tk.Frame(main_container, bg=BG_COLOR, bd=1, relief="solid")
    table_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Creating Canvas and Scrollbar
    canvas = Canvas(table_frame, bg=BG_COLOR, highlightthickness=0)
    scrollbar = Scrollbar(table_frame, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Binding the canvas resize event to the show_payment_details function
    canvas.bind("<Configure>", show_payment_details)

    # Displaying payment details in the canvas
    y_position = 20
    show_payment_details()

    make_payment.mainloop()

