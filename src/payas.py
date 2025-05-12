import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import StringVar
from datetime import datetime
import mysql.connector
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import qrcode
from PIL import Image, ImageTk
import subprocess
import threading

# Database connection
c = mysql.connector.connect(host="localhost", user="Admin", password="newpassword123", database="cfms")
cur = c.cursor()

# Google Drive API Setup
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "credentials.json"  # Path to your service account JSON file

# Authenticating with Google Drive
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Google Drive Folder ID where files will be uploaded
DRIVE_FOLDER_ID = "17PryBSaH9_M3dJ042A4sv3kru2UD9TBJ"

# Path to the output file
OUTPUT_FILE_PATH = "demand_prediction_output.png"


class MonthlyLogsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cashew Factory Management System - Monthly Logs")
        self.root.configure(background="#f0f0f0")
        self.root.state("zoomed")  # Maximize window

        try:
            self.root.iconbitmap("app_icon.ico")
        except:
            pass

        # Configuring grid weights for dynamic resizing
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=0)
        self.root.grid_rowconfigure(4, weight=0)
        self.root.grid_rowconfigure(5, weight=0)

        # Create styles for widgets
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Calm theme

        # Configuring colors
        bg_color = "#f0f0f0"
        header_bg = "#1e3d59"
        header_fg = "white"
        btn_color = "#ff6e40"
        btn_fg = "white"
        accent_color = "#ffc13b"

        # Configure components styles
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("Header.TLabel", background=header_bg, foreground=header_fg, font=("Segoe UI", 14, "bold"),
                             padding=10)
        self.style.configure("TButton", font=("Segoe UI", 11), background=btn_color, foreground=btn_fg)
        self.style.configure("Load.TButton", font=("Segoe UI", 12, "bold"), background=accent_color)
        self.style.configure("Save.TButton", font=("Segoe UI", 12, "bold"), background="#4CAF50", foreground="white")
        self.style.configure("Return.TButton", font=("Segoe UI", 11, "bold"), background="#f44336", foreground="white")

        # Configure Treeview
        self.style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background=header_bg,
                             foreground="white")
        self.style.map("Treeview", background=[("selected", accent_color)], foreground=[("selected", "black")])

        # Creating main frame with padding
        self.main_frame = ttk.Frame(root, style="TFrame", padding=(20, 20, 20, 20))
        self.main_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Header with title
        self.header_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ttk.Label(self.header_frame,
                                     text="MONTHLY LOGS MANAGEMENT",
                                     style="Header.TLabel",
                                     background=header_bg,
                                     foreground=header_fg)
        self.title_label.grid(row=0, column=0, sticky="ew")

        # Creating control panel frame
        self.control_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.control_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        # Configure control frame columns
        for i in range(6):
            self.control_frame.grid_columnconfigure(i, weight=1)

        # Area selection
        self.selected_module = StringVar()
        self.selected_module.set("Sales")  # Default to "Sales"

        self.module_label = ttk.Label(self.control_frame, text="Area:", font=("Segoe UI", 12, "bold"))
        self.module_label.grid(row=0, column=0, padx=(0, 5), pady=10, sticky="e")

        module_values = ["Sales", "Raw Material", "Production", "Stock Maintenance"]
        self.module_dropdown = ttk.Combobox(self.control_frame, textvariable=self.selected_module,
                                            values=module_values, state="readonly", width=20,
                                            font=("Segoe UI", 11))
        self.module_dropdown.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        # Month selection
        self.selected_month = StringVar()
        self.selected_month.set(datetime.now().strftime("%B"))  # current month by default

        self.month_label = ttk.Label(self.control_frame, text="Month:", font=("Segoe UI", 12, "bold"))
        self.month_label.grid(row=0, column=2, padx=(5, 5), pady=10, sticky="e")

        month_values = ["January", "February", "March", "April", "May", "June", "July",
                        "August", "September", "October", "November", "December"]
        self.month_dropdown = ttk.Combobox(self.control_frame, textvariable=self.selected_month,
                                           values=month_values, state="readonly", width=20,
                                           font=("Segoe UI", 11))
        self.month_dropdown.grid(row=0, column=3, padx=5, pady=10, sticky="w")

        # Load button
        self.load_button = tk.Button(self.control_frame, text="LOAD DATA", font=("Segoe UI", 11, "bold"),
                                     bg=accent_color, fg="black", padx=20, pady=8,
                                     relief=tk.RAISED, borderwidth=0,
                                     command=self.load_data,
                                     activebackground="#e8b935", activeforeground="black",
                                     cursor="hand2")
        self.load_button.grid(row=0, column=4, columnspan=2, padx=20, pady=10, sticky="ew")

        # Creating frame for the treeview
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)

        # Treeview with scrollbars
        self.tree = ttk.Treeview(self.tree_frame, columns=(), show="headings")

        # Vertical scrollbar
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")

        # Horizontal scrollbar
        hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=1, column=0, sticky="ew")

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Button frame
        self.button_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.button_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        # Save button (Uploads to Google Drive)
        self.save_button = tk.Button(self.button_frame, text="SAVE TO GOOGLE DRIVE",
                                     font=("Segoe UI", 11, "bold"),
                                     bg="#4CAF50", fg="white",
                                     padx=20, pady=10,
                                     relief=tk.RAISED, borderwidth=0,
                                     command=self.upload_to_drive,
                                     activebackground="#45a049", activeforeground="white",
                                     cursor="hand2")
        self.save_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Return to main page button
        self.return_button = tk.Button(self.button_frame, text="RETURN TO MAIN PAGE",
                                       font=("Segoe UI", 11, "bold"),
                                       bg="#f44336", fg="white",
                                       padx=20, pady=10,
                                       relief=tk.RAISED, borderwidth=0,
                                       command=self.return_to_main_page,
                                       activebackground="#d32f2f", activeforeground="white",
                                       cursor="hand2")
        self.return_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # QR code frame
        self.qr_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.qr_frame.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        self.qr_frame.grid_columnconfigure(0, weight=1)

        # Status bar at the bottom
        self.status_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.status_frame.grid(row=6, column=0, sticky="ew", pady=(10, 0))

        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var,
                                      font=("Segoe UI", 10), anchor="w")
        self.status_label.grid(row=0, column=0, sticky="w")

        # Generating and displaying QR code
        #self.generate_qr_code()

    def run(self):
        self.root.mainloop()

    def load_data(self):
        """Loading data based on selected month and domain"""
        self.status_var.set("Loading data...")
        selected_month = self.selected_month.get()
        selected_module = self.selected_module.get()

        # Converting month to number
        month_number = datetime.strptime(selected_month, "%B").month

        # Clear previous data
        self.tree.delete(*self.tree.get_children())

        # Configuring the column widths based on the module
        for col in self.tree["columns"]:
            self.tree.column(col, width=100)  # Default width

        if selected_module == "Sales":
            self.load_sells_data(month_number)
        elif selected_module == "Raw Material":
            self.load_raw_material_data(month_number)
        elif selected_module == "Production":
            self.load_production_data(month_number)
        elif selected_module == "Stock Maintenance":
            self.load_stock_maintenance_data(month_number)

        self.status_var.set(f"Data loaded for {selected_month} - {selected_module}")

    def load_sells_data(self, month):
        """Loading sales data for the selected month."""
        self.tree["columns"] = ("Date", "Client", "Item", "Quantity", "Rate", "Total", "Paid")

        # Configuring columns with appropriate widths
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Client", width=150, anchor="w")
        self.tree.column("Item", width=150, anchor="w")
        self.tree.column("Quantity", width=100, anchor="e")
        self.tree.column("Rate", width=100, anchor="e")
        self.tree.column("Total", width=100, anchor="e")
        self.tree.column("Paid", width=100, anchor="center")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Getting first and last date of the selected month
        first_day = f"{datetime.now().year}-{month:02d}-01"
        last_day = f"{datetime.now().year}-{month:02d}-28"

        cur.execute(
            "SELECT adate, client, item, quantity, rate, total, paid FROM sell WHERE adate BETWEEN %s AND %s",
            (first_day, last_day))
        rows = cur.fetchall()

        if not rows:
            self.tree.insert("", "end", values=("No data available", "", "", "", "", "", ""), tags=("nodata",))
            self.style.configure("Treeview", rowheight=50)  # Increasing row height for empty state
        else:
            for i, row in enumerate(rows):
                formatted_row = list(row)
                if isinstance(row[0], datetime):
                    formatted_row[0] = row[0].strftime("%Y-%m-%d")

                # Formatting numbers for
                if row[3]:  # Quantity
                    formatted_row[3] = f"{float(row[3]):,.2f}"
                if row[4]:  # Rate
                    formatted_row[4] = f"₹{float(row[4]):,.2f}"
                if row[5]:  # Total
                    formatted_row[5] = f"₹{float(row[5]):,.2f}"

                # Alternate row colors
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", "end", values=formatted_row, tags=(tag,))

            # Configuring row color tags
            self.style.map("Treeview", background=[("selected", "#ffc13b")])
            self.style.configure("Treeview", rowheight=25)  # Reset row height

        # Adding tag configurations for even/odd rows
        self.tree.tag_configure("even", background="#f5f5f5")
        self.tree.tag_configure("odd", background="white")
        self.tree.tag_configure("nodata", background="#f0f0f0")

    def load_raw_material_data(self, month):
        """Loading raw material data for the selected month."""
        self.tree["columns"] = ("Date", "Raw Material", "Item Type", "Quantity")

        # Configure columns with appropriate widths
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Raw Material", width=150, anchor="w")
        self.tree.column("Item Type", width=150, anchor="w")
        self.tree.column("Quantity", width=100, anchor="e")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # To get first and last date of the selected month
        first_day = f"{datetime.now().year}-{month:02d}-01"
        last_day = f"{datetime.now().year}-{month:02d}-28"

        cur.execute(
            "SELECT adate, raw, item_type, quantity FROM raw_material WHERE adate BETWEEN %s AND %s",
            (first_day, last_day))
        rows = cur.fetchall()

        if not rows:
            self.tree.insert("", "end", values=("No data available", "", "", ""), tags=("nodata",))
            self.style.configure("Treeview", rowheight=50)  # Increasing row height for empty state
        else:
            for i, row in enumerate(rows):
                formatted_row = list(row)
                if isinstance(row[0], datetime):
                    formatted_row[0] = row[0].strftime("%Y-%m-%d")

                # Formatting numbers
                if row[3]:  # Quantity
                    formatted_row[3] = f"{float(row[3]):,.2f} kg"

                # Alternate row colors
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", "end", values=formatted_row, tags=(tag,))

            # Configuring row color tags
            self.style.map("Treeview", background=[("selected", "#ffc13b")])
            self.style.configure("Treeview", rowheight=25)  # Resetting row height

        # Add tag configurations for even/odd rows
        self.tree.tag_configure("even", background="#f5f5f5")
        self.tree.tag_configure("odd", background="white")
        self.tree.tag_configure("nodata", background="#f0f0f0")

    def load_production_data(self, month):
        """Loading production data for the selected month."""
        self.tree["columns"] = ("Date", "Item Type", "Grade A", "Grade B", "Grade C")

        # Configure columns with appropriate widths
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Item Type", width=150, anchor="w")
        self.tree.column("Grade A", width=100, anchor="e")
        self.tree.column("Grade B", width=100, anchor="e")
        self.tree.column("Grade C", width=100, anchor="e")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Get first and last date of the selected month
        first_day = f"{datetime.now().year}-{month:02d}-01"
        last_day = f"{datetime.now().year}-{month:02d}-28"

        cur.execute(
            "SELECT adate, item_type, sa, sb, sc FROM production WHERE adate BETWEEN %s AND %s",
            (first_day, last_day))
        rows = cur.fetchall()

        if not rows:
            self.tree.insert("", "end", values=("No data available", "", "", "", ""), tags=("nodata",))
            self.style.configure("Treeview", rowheight=50)  # Increasing row height for empty state
        else:
            for i, row in enumerate(rows):
                # Format date if needed
                formatted_row = list(row)
                if isinstance(row[0], datetime):
                    formatted_row[0] = row[0].strftime("%Y-%m-%d")

                # Formatting numbers
                for j in range(2, 5):  # Columns 2, 3, 4 (Grade A, B, C)
                    if row[j] is not None:
                        formatted_row[j] = f"{float(row[j]):,.2f} kg"

                # Alternate row colors
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", "end", values=formatted_row, tags=(tag,))

            # Configure row color tags
            self.style.map("Treeview", background=[("selected", "#ffc13b")])
            self.style.configure("Treeview", rowheight=25)  # Reset row height

        # Adding tag configurations for even/odd rows
        self.tree.tag_configure("even", background="#f5f5f5")
        self.tree.tag_configure("odd", background="white")
        self.tree.tag_configure("nodata", background="#f0f0f0")

    def load_stock_maintenance_data(self, month):
        """Loading stock maintenance data for the selected month."""
        self.tree["columns"] = ("Date", "Region", "Cashew Type", "Change")

        # Configure columns with appropriate widths
        self.tree.column("Date", width=120, anchor="center")
        self.tree.column("Region", width=150, anchor="w")
        self.tree.column("Cashew Type", width=150, anchor="w")
        self.tree.column("Change", width=120, anchor="e")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Get first and last date of the selected month
        first_day = f"{datetime.now().year}-{month:02d}-01"
        last_day = f"{datetime.now().year}-{month:02d}-28"

        cur.execute(
            "SELECT timestamp, region, cashew_type, `change` FROM stock_changes WHERE timestamp BETWEEN %s AND %s",
            (first_day, last_day))
        rows = cur.fetchall()

        if not rows:
            self.tree.insert("", "end", values=("No data available", "", "", ""), tags=("nodata",))
            self.style.configure("Treeview", rowheight=50)  # Increasing row height for empty state
        else:
            for i, row in enumerate(rows):
                # Format date if needed
                formatted_row = list(row)
                if isinstance(row[0], datetime):
                    formatted_row[0] = row[0].strftime("%Y-%m-%d %H:%M")

                # Formatting numbers
                if row[3]:  # Change
                    if float(row[3]) > 0:
                        formatted_row[3] = f"+{float(row[3]):,.2f} kg"
                    else:
                        formatted_row[3] = f"{float(row[3]):,.2f} kg"

                # Alternate row colors
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", "end", values=formatted_row, tags=(tag,))

            # Configure row color tags
            self.style.map("Treeview", background=[("selected", "#ffc13b")])
            self.style.configure("Treeview", rowheight=25)  # Reset row height

        # Adding tag configurations for even/odd rows
        self.tree.tag_configure("even", background="#f5f5f5")
        self.tree.tag_configure("odd", background="white")
        self.tree.tag_configure("nodata", background="#f0f0f0")

    def upload_to_drive(self):
        """Saving and uploading data to Google Drive"""
        selected_module = self.selected_module.get()

        # File name
        file_name = f"{selected_module}_{datetime.now().strftime('%Y-%m')}.xlsx"

        # To prepare data for saving
        data = []
        columns = self.tree["columns"]
        for item in self.tree.get_children():
            row = self.tree.item(item)["values"]
            data.append(row)

        # Creating DataFrame
        df = pd.DataFrame(data, columns=columns)

        # Saving the file temporarily
        temp_file_path = f"{file_name}"  # Store it in the working directory
        df.to_excel(temp_file_path, index=False)

        # Authenticate Google Drive API
        drive_service = build("drive", "v3", credentials=creds)

        # Upload file to Google Drive
        try:
            file_metadata = {
                "name": file_name,
                "parents": [DRIVE_FOLDER_ID],  # Uploading it to the specified folder
            }
            media = MediaFileUpload(temp_file_path,
                                    mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

            messagebox.showinfo("Success", f"Data uploaded successfully to Google Drive: {file_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload data: {e}")

    def return_to_main_page(self):
        """Closing current window and back to index.py"""
        self.root.destroy()  # Closing the current window


def main():
    root = tk.Tk()
    app = MonthlyLogsApp(root)
    app.run()


if __name__ == "__main__":
    main()






