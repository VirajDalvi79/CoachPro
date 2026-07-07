import customtkinter as ctk
from tkinter import filedialog
import shutil
import os
import subprocess
import datetime

from ui.theme import COLORS, FONTS
from ui.components.dialogs import show_success, show_error
from settings_manager import SettingsManager


class SettingsPage(ctk.CTkFrame):

    def __init__(self, master, admin_info=None):
        super().__init__(master, fg_color="transparent")

        self.manager = SettingsManager()

        self._build_ui()
        self.load_settings()

    def _build_ui(self):

        ctk.CTkLabel(
            self,
            text="Settings",
            font=FONTS["h1"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 16))

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.scroll.pack(fill="both", expand=True)

        # ---------------- Institute Info ----------------

        info_card = self._card("Institute Information")

        self.name_entry = self._field(info_card, "Institute Name")
        self.address_entry = self._field(info_card, "Address")
        self.phone_entry = self._field(info_card, "Phone")
        self.email_entry = self._field(info_card, "Email")

        

        # ---------------- Branding ----------------

        branding_card = self._card("Branding")

        self.logo_path_entry = self._field(branding_card, "Logo Path")

        ctk.CTkButton(
            branding_card,
            text="Choose Logo",
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["accent"],
            command=self.choose_logo,
        ).pack(anchor="w", padx=20, pady=(12, 20))

        # ---------------- Database ----------------

        database_card = self._card("Database")

        ctk.CTkButton(
            database_card,
            text="Backup Database",
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["accent"],
            command=self.backup_database,
        ).pack(anchor="w", padx=20, pady=(12, 20))

        # ---------------- Save ----------------

        save_card = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent",
        )
        save_card.pack(fill="x", pady=(10, 30))

        ctk.CTkButton(
            save_card,
            text="Save Settings",
            height=44,
            width=180,
            corner_radius=12,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self.save_settings,
        ).pack(anchor="e", padx=10)

    def _card(self, title):

        card = ctk.CTkFrame(
            self.scroll,
            fg_color=COLORS["bg_surface"],
            corner_radius=14,
            border_width=1,
            border_color=COLORS["border"],
        )
        card.pack(fill="x", padx=10, pady=(0, 16))

        ctk.CTkLabel(
            card,
            text=title,
            font=FONTS["h2"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=20, pady=(18, 8))

        return card

    def _field(self, parent, label):

        ctk.CTkLabel(
            parent,
            text=label,
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=20, pady=(10, 4))

        entry = ctk.CTkEntry(
            parent,
            width=460,
            height=38,
            corner_radius=10,
        )
        entry.pack(anchor="w", padx=20)

        return entry

    def load_settings(self):

        settings = self.manager.load_settings()

        self.name_entry.insert(0, settings.get("institute_name", ""))
        self.address_entry.insert(0, settings.get("address", ""))
        self.phone_entry.insert(0, settings.get("phone", ""))
        self.email_entry.insert(0, settings.get("email", ""))
        self.logo_path_entry.insert(0, settings.get("logo_path", ""))

        

    def save_settings(self):

        try:
            settings = {
                "institute_name": self.name_entry.get().strip(),
                "address": self.address_entry.get().strip(),
                "phone": self.phone_entry.get().strip(),
                "email": self.email_entry.get().strip(),
                "logo_path": self.logo_path_entry.get().strip(),
            }

            self.manager.save_settings(settings)

            

            show_success(
                self,
                "Settings saved successfully."
            )

        except Exception as e:
            show_error(
                self,
                "Error",
                str(e)
            )

    def choose_logo(self):

        file_path = filedialog.askopenfilename(
            title="Choose Institute Logo",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg")
            ]
        )

        if not file_path:
            return

        os.makedirs("assets", exist_ok=True)

        ext = os.path.splitext(file_path)[1]
        new_path = os.path.join("assets", f"institute_logo{ext}")

        shutil.copy(file_path, new_path)

        self.logo_path_entry.delete(0, "end")
        self.logo_path_entry.insert(0, new_path)

    def backup_database(self):

        backup_folder = "backups"
        os.makedirs(backup_folder, exist_ok=True)

        file_name = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        file_path = os.path.join(backup_folder, file_name)

        try:
            command = [
                "mysqldump",
                "-u", "root",
                "-pPassword",
                "coaching_management_system"
            ]

            with open(file_path, "w", encoding="utf-8") as backup_file:
                subprocess.run(
                    command,
                    stdout=backup_file,
                    check=True
                )

            show_success(
                self,
                f"Backup created:\n{file_path}"
            )

        except Exception as e:
            show_error(
                self,
                "Backup Failed",
                str(e)
            )