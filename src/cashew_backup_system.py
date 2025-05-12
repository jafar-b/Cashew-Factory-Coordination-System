import os
import datetime
import time
import tempfile
import threading
import tkinter as tk
from tkinter import messagebox
import gc
import subprocess
import atexit
import signal
import sys
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

class BackupSystem:
    # Configuration
    DB_HOST = "localhost"
    DB_USER = "Admin"
    DB_PASSWORD = "newpassword123"
    DB_NAME = "cfms"
    GOOGLE_DRIVE_CREDENTIALS = "credentials.json"
    GOOGLE_DRIVE_FOLDER_ID = "17PryBSaH9_M3dJ042A4sv3kru2UD9TBJ"

    # System state
    _initialized = False
    _backup_dir = os.path.join(tempfile.gettempdir(), "cashew_backups")
    _logger = None

    @classmethod
    def init_system(cls):
        """Initialize backup system with all protections"""
        if not cls._initialized:
            cls._setup_logging()
            cls._setup_directories()
            cls._setup_emergency_handlers()
            cls._patch_tkinter()
            cls.schedule_automatic_backups()
            cls._initialized = True
            cls._logger.info("Backup system initialized successfully")

    @classmethod
    def _setup_logging(cls):
        """Configure logging for the backup system"""
        log_file = os.path.join(cls._backup_dir, "backup_system.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        cls._logger = logging.getLogger("CashewBackup")
        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

    @classmethod
    def _setup_directories(cls):
        """Create necessary directories"""
        os.makedirs(cls._backup_dir, exist_ok=True)

    @classmethod
    def _setup_emergency_handlers(cls):
        """Set up handlers for emergency situations"""
        atexit.register(cls._emergency_backup)
        signal.signal(signal.SIGTERM, cls._handle_signal)
        signal.signal(signal.SIGINT, cls._handle_signal)
        sys.excepthook = cls._handle_exception

    @classmethod
    def _handle_signal(cls, signum, frame):
        """Handle system signals"""
        cls._logger.warning(f"Received termination signal {signum}")
        cls._emergency_backup()
        sys.exit(0)

    @classmethod
    def _handle_exception(cls, exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions"""
        cls._logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        cls._emergency_backup()
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    @classmethod
    def _emergency_backup(cls):
        """Perform emergency backup"""
        try:
            cls._logger.warning("Performing emergency backup")
            cls.run_backup(show_message=False)
        except Exception as e:
            cls._logger.error(f"Emergency backup failed: {str(e)}")

    @classmethod
    def _patch_tkinter(cls):
        """Monkey-patch Tk/Toplevel to auto-add backup button"""
        original_tk_init = tk.Tk.__init__
        original_toplevel_init = tk.Toplevel.__init__

        def patched_tk_init(self, *args, **kwargs):
            original_tk_init(self, *args, **kwargs)
            cls.add_backup_button(self)

        def patched_toplevel_init(self, *args, **kwargs):
            original_toplevel_init(self, *args, **kwargs)
            cls.add_backup_button(self)

        tk.Tk.__init__ = patched_tk_init
        tk.Toplevel.__init__ = patched_toplevel_init

    @classmethod
    def add_backup_button(cls, window):
        """Add backup button with guaranteed visibility"""
        try:
            # Create a dedicated frame for the button
            btn_frame = tk.Frame(window)
            btn_frame.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

            # Backup button
            btn = tk.Button(
                btn_frame,
                text="🚨 BACKUP 🚨",
                command=cls.run_backup,
                bg="#ff0000",
                fg="white",
                font=("Arial", 10, "bold"),
                borderwidth=3,
                relief="raised"
            )
            btn.pack()

            # Forcing window update to ensure button appears
            window.update_idletasks()

            #cls._logger.info(f"Backup button added to {window}")

        except Exception as e:
            cls._logger.error(f"Failed to add backup button: {str(e)}")

    @classmethod
    def _get_drive_service(cls):
        """Get authenticated Google Drive service with JWT fix"""
        try:
            creds = service_account.Credentials.from_service_account_file(
                cls.GOOGLE_DRIVE_CREDENTIALS,
                scopes=['https://www.googleapis.com/auth/drive.file']
            )

            # Refresh token if needed
            if creds.expired:
                creds.refresh(Request())

            return build('drive', 'v3', credentials=creds)
        except Exception as e:
            cls._logger.error(f"Google Drive authentication failed: {str(e)}")
            return None

    @classmethod
    def run_backup(cls, show_message=True):
        """Main backup method - Silently skips Google Drive errors"""
        backup_file = None
        conn = None

        try:
            # Create backup file
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(cls._backup_dir, f"cashew_backup_{timestamp}.sql")
            temp_path = backup_file + '.tmp'

            # Database backup
            import mysql.connector
            conn = mysql.connector.connect(
                host=cls.DB_HOST,
                user=cls.DB_USER,
                password=cls.DB_PASSWORD,
                database=cls.DB_NAME
            )
            cursor = conn.cursor()

            with open(temp_path, 'w', encoding='utf-8') as f:
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]

                for table in tables:
                    cursor.execute(f"SHOW CREATE TABLE `{table}`")
                    create_table = cursor.fetchone()[1]
                    f.write(f"{create_table};\n\n")

                    cursor.execute(f"SELECT * FROM `{table}`")
                    rows = cursor.fetchall()
                    if rows:
                        columns = [i[0] for i in cursor.description]
                        f.write(f"INSERT INTO `{table}` ({','.join(columns)}) VALUES\n")
                        for row in rows:
                            values = []
                            for v in row:
                                if v is None:
                                    values.append("NULL")
                                else:
                                    values.append(f"'{str(v).replace("'", "''")}'")
                            f.write(f"({','.join(values)}),\n")
                        f.write(";\n\n")

            os.rename(temp_path, backup_file)
            cls._logger.info(f"Local backup created: {backup_file}")

            # Google Drive Upload
            if os.path.exists(cls.GOOGLE_DRIVE_CREDENTIALS):
                service = cls._get_drive_service()
                if service:
                    try:
                        file_metadata = {
                            'name': os.path.basename(backup_file),
                            'parents': [cls.GOOGLE_DRIVE_FOLDER_ID]
                        }
                        media = MediaFileUpload(backup_file, mimetype='application/sql')
                        service.files().create(
                            body=file_metadata,
                            media_body=media,
                            fields='id'
                        ).execute()
                        cls._logger.info("Backup uploaded to Google Drive")
                    except Exception as e:
                        cls._logger.error(f"[Silenced] Google Drive upload failed: {str(e)}")


            if show_message:
                messagebox.showinfo("Success", "Backup completed successfully!")
            return True

        except Exception as e:
            cls._logger.error(f"Backup failed: {str(e)}")
            if show_message:
                messagebox.showerror("Error", f"Backup failed: {str(e)}")
            return False

        finally:
            # Cleanup resources
            if conn and conn.is_connected():
                conn.close()
            if backup_file and os.path.exists(backup_file):
                try:
                    os.remove(backup_file)
                except:
                    pass
            temp_path = backup_file + '.tmp' if backup_file else None
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass

    @classmethod
    def schedule_automatic_backups(cls):
        """Schedule regular background backups"""
        def backup_loop():
            while True:
                time.sleep(24 * 3600)  # 24 hours
                try:
                    cls._logger.info("Running scheduled backup")
                    cls.run_backup(show_message=False)
                except Exception as e:
                    cls._logger.error(f"Scheduled backup failed: {str(e)}")

        thread = threading.Thread(target=backup_loop, daemon=True)
        thread.start()
