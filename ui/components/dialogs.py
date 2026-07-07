"""
ui/components/dialogs.py

Reusable modal dialogs: confirmation prompts and success/error popups,
themed to match the rest of the app. Every delete/deactivate needs a
confirmation dialog and every success/failure needs a popup per the
User Experience Rules doc — this is the one place those are defined.
"""

import customtkinter as ctk
from ui.theme import COLORS, FONTS


class _BaseDialog(ctk.CTkToplevel):
    def __init__(self, master, title, width=380, height=200):
        super().__init__(master)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg_surface"])
        self.transient(master)
        self.grab_set()
        self._center(master, width, height)

    def _center(self, master, width, height):
        self.update_idletasks()
        x = master.winfo_rootx() + (master.winfo_width() // 2) - (width // 2)
        y = master.winfo_rooty() + (master.winfo_height() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


class ConfirmDialog(_BaseDialog):
    def __init__(self, master, title, message, on_confirm, confirm_text="Confirm", danger=False):
        super().__init__(master, title, width=380, height=190)
        self.on_confirm = on_confirm

        ctk.CTkLabel(
            self, text=message, font=FONTS["body"], text_color=COLORS["text_primary"],
            wraplength=320, justify="left"
        ).pack(padx=24, pady=(28, 20))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(0, 20))

        ctk.CTkButton(
            btn_row, text="Cancel", width=120, height=36, corner_radius=8,
            fg_color=COLORS["bg_surface_alt"], hover_color=COLORS["border"],
            text_color=COLORS["text_secondary"], command=self.destroy
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btn_row, text=confirm_text, width=120, height=36, corner_radius=8,
            fg_color=COLORS["error"] if danger else COLORS["accent"],
            hover_color="#B91C1C" if danger else COLORS["accent_hover"],
            command=self._confirm
        ).pack(side="left", padx=8)

    def _confirm(self):
        self.destroy()
        self.on_confirm()


class InfoDialog(_BaseDialog):
    def __init__(self, master, title, message, success=True):
        super().__init__(master, title, width=360, height=170)
        color = COLORS["success"] if success else COLORS["error"]
        icon = "✓" if success else "✕"

        ctk.CTkLabel(
            self, text=icon, font=(FONTS["h1"][0], 30, "bold"), text_color=color
        ).pack(pady=(24, 6))

        ctk.CTkLabel(
            self, text=message, font=FONTS["body"], text_color=COLORS["text_primary"],
            wraplength=300, justify="center"
        ).pack(padx=20)

        ctk.CTkButton(
            self, text="OK", width=100, height=32, corner_radius=8,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=self.destroy
        ).pack(pady=18)


def show_success(master, message, title="Success"):
    InfoDialog(master, title, message, success=True)


def show_error(master, message, title="Error"):
    InfoDialog(master, title, message, success=False)
