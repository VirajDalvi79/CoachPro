import customtkinter as ctk

from admin import Admin
from ui.theme import COLORS, FONTS
from ui.components.dialogs import show_error, show_success


class SetupAdminWindow(ctk.CTk):

    def __init__(self, on_success):
        super().__init__()

        self.on_success = on_success
        self.admin_backend = Admin()

        self.title("Create Admin")
        self.geometry("420x620")
        self.minsize(420, 620)
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg_app"])

        self._build_ui()

    def _build_ui(self):
        card = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_surface"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        card.pack(fill="both", expand=True, padx=28, pady=28)

        ctk.CTkLabel(
            card,
            text="First-Time Setup",
            font=FONTS["h1"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=24, pady=(28, 6))

        ctk.CTkLabel(
            card,
            text="Create the owner admin account.",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=24, pady=(0, 18))

        self.full_name_entry = self._field(card, "Full Name")
        self.username_entry = self._field(card, "Username")
        self.password_entry = self._field(card, "Password", show="*")
        self.confirm_entry = self._field(card, "Confirm Password", show="*")

        self.error_label = ctk.CTkLabel(
            card,
            text="",
            font=FONTS["small"],
            text_color=COLORS["error"],
            wraplength=330,
        )
        self.error_label.pack(anchor="w", padx=24, pady=(10, 0))

        ctk.CTkButton(
            card,
            text="Create Admin",
            height=42,
            corner_radius=12,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self.create_admin,
        ).pack(fill="x", padx=24, pady=(18, 40))

    def _field(self, parent, label, show=None):
        ctk.CTkLabel(
            parent,
            text=label,
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=24, pady=(10, 4))

        entry = ctk.CTkEntry(
            parent,
            height=38,
            corner_radius=10,
            show=show,
        )
        entry.pack(fill="x", padx=24)
        return entry

    def create_admin(self):
        full_name = self.full_name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        if not full_name or not username or not password:
            self.error_label.configure(text="All fields are required.")
            return

        if password != confirm:
            self.error_label.configure(text="Passwords do not match.")
            return

        if len(password) < 6:
            self.error_label.configure(text="Password must be at least 6 characters.")
            return

        try:
            self.admin_backend.create_admin(
                username=username,
                password=password,
                full_name=full_name,
                role="ADMIN",
            )

            show_success(self, "Admin created successfully. Please log in.")
            self.destroy()
            self.on_success()

        except Exception as e:
            self.error_label.configure(text=f"Could not create admin: {e}")