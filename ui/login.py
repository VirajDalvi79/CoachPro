"""
ui/login.py

Phase 1 — Admin Login screen. Standalone CTk window shown before the
main application. On successful authentication it closes itself and
hands control to the main application window via the on_success
callback (passed in from main.py, so this file never needs to know
about MainWindow directly).
"""

import customtkinter as ctk
from tkinter import messagebox


from admin import Admin
from ui.theme import COLORS, FONTS


class LoginWindow(ctk.CTk):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.admin_backend = Admin()

        self.title("Coaching Management System — Login")
        self.geometry("420x480")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg_app"])

        self._center_window()
        self._build_ui()

        

    def _center_window(self):
        self.update_idletasks()
        w, h = 420, 480
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        card = ctk.CTkFrame(
            self, fg_color=COLORS["bg_surface"], corner_radius=16,
            border_width=1, border_color=COLORS["border"]
        )
        card.pack(expand=True, fill="both", padx=30, pady=30)

        ctk.CTkLabel(
            card, text="Coaching Management System",
            font=FONTS["h2"], text_color=COLORS["text_primary"],
            wraplength=280, justify="center"
        ).pack(pady=(40, 4))

        ctk.CTkLabel(
            card, text="Sign in to continue",
            font=FONTS["body"], text_color=COLORS["text_secondary"]
        ).pack(pady=(0, 30))

        self.username_entry = ctk.CTkEntry(
            card, placeholder_text="Username", width=260, height=40,
            corner_radius=8
        )
        self.username_entry.pack(pady=8)
        self.username_entry.focus()

        self.password_entry = ctk.CTkEntry(
            card, placeholder_text="Password", show="•", width=260,
            height=40, corner_radius=8
        )
        self.password_entry.pack(pady=8)
        self.password_entry.bind("<Return>", lambda e: self._handle_login())

        self.error_label = ctk.CTkLabel(
            card, text="", font=FONTS["small"], text_color=COLORS["error"],
            wraplength=260
        )
        self.error_label.pack(pady=(4, 0))

        ctk.CTkButton(
            card, text="Log In", width=260, height=40, corner_radius=8,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            font=FONTS["button"], command=self._handle_login
        ).pack(pady=(20, 10))

    def _handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.configure(text="Enter both username and password")
            return


        admin_info = self.admin_backend.authenticate(username, password)

        if admin_info is None:
            self.error_label.configure(text="Invalid username or password")
            self.password_entry.delete(0, "end")
            return

        self.destroy()
        self.on_success(admin_info)

    def _show_db_error(self):
        self.error_label.configure(
            text="Cannot reach the database. Check the server and try again."
        )
        messagebox.showerror(
            "Database Unavailable",
            "Could not connect to MySQL.\n\n"
            "Check that the database server is running and that "
            "DB_HOST / DB_USER / DB_PASSWORD / DB_NAME are set correctly."
        )
