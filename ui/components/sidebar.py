"""
ui/components/sidebar.py

Reusable sidebar navigation.
The sidebar only renders navigation buttons.
It does NOT automatically navigate to a page.
"""

import customtkinter as ctk
from ui.theme import COLORS, FONTS
from settings_manager import SettingsManager
import os
from PIL import Image


NAV_ITEMS = [
    ("dashboard", "Dashboard", True),
    ("students", "Students", True),
    ("batches", "Batches", True),
    ("attendance", "Attendance", True),
    ("marks", "Marks", True),
    ("fees", "Fees", True),
    ("reports", "Reports", True),
    ("exams", "Exams", True),
    ("subjects", "Subjects", True),
    ("settings", "Settings", True),

]


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, on_navigate, on_logout, admin_name):
        super().__init__(
            master,
            fg_color=COLORS["bg_sidebar"],
            corner_radius=0,
            width=220,
        )

        self.pack_propagate(False)

        self.on_navigate = on_navigate
        self.on_logout = on_logout

        self.buttons = {}
        self.settings_manager = SettingsManager()
        self.settings = self.settings_manager.load_settings()

        self._build_header(admin_name)
        self._build_nav()
        self._build_footer()

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    def _build_header(self, admin_name):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(25, 20),
        )

        logo_path = self.settings.get("logo_path", "")

        if logo_path and os.path.exists(logo_path):

         self.logo_image = ctk.CTkImage(
         light_image=Image.open(logo_path),
         dark_image=Image.open(logo_path),
         size=(48, 48)
    )

         ctk.CTkLabel(
         header,
          image=self.logo_image,
        text=""
    ).pack(anchor="w", pady=(0, 10))

        else:

         ctk.CTkLabel(
        header,
        text="🏫",
        font=("Segoe UI Emoji", 34),
    ).pack(anchor="w", pady=(0, 10))
        

        ctk.CTkLabel(
            header,
            text=self.settings.get("institute_name", "CoachPro Academy"),
            font=FONTS["h2"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text=f"Signed in as\n{admin_name}",
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
            justify="left",
        ).pack(anchor="w", pady=(5, 0))

        ctk.CTkFrame(
            self,
            height=1,
            fg_color=COLORS["border"],
        ).pack(
            fill="x",
            padx=20,
        )

    # --------------------------------------------------
    # Navigation
    # --------------------------------------------------

    def _build_nav(self):

        nav = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        nav.pack(
            fill="x",
            padx=12,
            pady=12,
        )

        for key, text, enabled in NAV_ITEMS:

            button = ctk.CTkButton(
                nav,
                text=text,
                anchor="w",
                height=42,
                corner_radius=8,
                fg_color="transparent",
                hover_color=COLORS["bg_surface_alt"],
                text_color=COLORS["text_primary"] if enabled else COLORS["text_muted"],
                font=FONTS["body"],
                state="normal" if enabled else "disabled",
                command=(lambda k=key: self._select(k)) if enabled else None,
            )

            button.pack(
                fill="x",
                pady=3,
            )

            self.buttons[key] = button

        # IMPORTANT:
        # Do NOT call self._select("dashboard") here.
        # MainWindow will select the first page after it
        # has finished creating the content frame.

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------

    def _build_footer(self):

        ctk.CTkFrame(
            self,
            height=1,
            fg_color=COLORS["border"],
        ).pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=(0, 12),
        )

        logout = ctk.CTkButton(
            self,
            text="Log Out",
            height=40,
            corner_radius=8,
            fg_color="transparent",
            hover_color=COLORS["error"],
            text_color=COLORS["text_secondary"],
            font=FONTS["body"],
            command=self.on_logout,
        )

        logout.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=(0, 20),
        )

    # --------------------------------------------------
    # Selection
    # --------------------------------------------------

    def _select(self, key):

        for page, button in self.buttons.items():

            if button.cget("state") == "disabled":
                continue

            if page == key:

                button.configure(
                    fg_color=COLORS["accent_soft"],
                    text_color=COLORS["text_primary"],
                )

            else:

                button.configure(
                    fg_color="transparent",
                    text_color=COLORS["text_muted"],
                )

        self.on_navigate(key)