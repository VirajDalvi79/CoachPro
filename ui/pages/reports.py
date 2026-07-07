import datetime
import customtkinter as ctk
from tkinter import ttk

from ui.theme import COLORS, FONTS
from reports import ReportsBackend


class ReportsPage(ctk.CTkFrame):

    def __init__(self, master, admin_info=None):
        super().__init__(master, fg_color="transparent")

        self.reports_backend = ReportsBackend()

        self._build_ui()
        self.load_reports()

    def _build_ui(self):

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            header,
            text="Reports Dashboard",
            font=FONTS["h1"],
            text_color=COLORS["text_primary"]
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="Refresh",
            command=self.load_reports,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"]
        ).pack(side="right")

        cards = ctk.CTkFrame(self, fg_color="transparent")
        cards.pack(fill="x", pady=10)

        self.total_students_card = self._card(cards, "Total Students", "0", 0, 0)
        self.active_students_card = self._card(cards, "Active Students", "0", 0, 1)
        self.batch_card = self._card(cards, "Total Batches", "0", 0, 2)
        self.attendance_card = self._card(cards, "Today's Attendance", "0", 0, 3)

        self.total_fee_card = self._card(cards, "Total Fees", "₹0", 1, 0)
        self.collected_card = self._card(cards, "Collected", "₹0", 1, 1)
        self.pending_card = self._card(cards, "Pending", "₹0", 1, 2)

        section = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_surface"],
            corner_radius=12
        )
        section.pack(fill="both", expand=True, pady=15)

        ctk.CTkLabel(
            section,
            text="Recent Payments",
            font=FONTS["h2"],
            text_color=COLORS["text_primary"]
        ).pack(anchor="w", padx=15, pady=12)

        self.tree = ttk.Treeview(
            section,
            columns=("student", "amount", "date", "remarks"),
            show="headings"
        )

        self.tree.heading("student", text="Student")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("date", text="Date")
        self.tree.heading("remarks", text="Remarks")

        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _card(self, parent, title, value, row, column):

        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_surface"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        card.grid(row=row, column=column, padx=8, pady=8, sticky="nsew")

        parent.grid_columnconfigure(column, weight=1)

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=FONTS["h2"],
            text_color=COLORS["text_primary"]
        )
        value_label.pack(anchor="w", padx=15, pady=(15, 2))

        ctk.CTkLabel(
            card,
            text=title,
            font=FONTS["small"],
            text_color=COLORS["text_secondary"]
        ).pack(anchor="w", padx=15, pady=(0, 15))

        return value_label

    

    def load_reports(self):

        today = datetime.date.today()

        total_students, active_students, inactive_students = self.reports_backend.student_summary()
        batch_count = self.reports_backend.batch_count()
        total_marked, present, absent = self.reports_backend.today_attendance_summary(today)
        total_fee, collected, pending = self.reports_backend.fees_summary()

        self.total_students_card.configure(text=str(total_students or 0))
        self.active_students_card.configure(text=str(active_students or 0))
        self.batch_card.configure(text=str(batch_count or 0))

        attendance_text = f"{present or 0}/{total_marked or 0}"
        self.attendance_card.configure(text=attendance_text)

        self.total_fee_card.configure(text=self.money(total_fee or 0))
        self.collected_card.configure(text=self.money(collected or 0))
        self.pending_card.configure(text=self.money(pending or 0))

        self.tree.delete(*self.tree.get_children())

        for student, amount, payment_date, remarks in self.reports_backend.recent_payments():
            self.tree.insert(
                "",
                "end",
                values=(
                    student,
                    self.money(amount),
                    payment_date,
                    remarks or "—"
                )
            )

    def money(self, amount):
     return f"₹{float(amount):,.2f}"

    def student_id(self, sid):
     return f"STU-{int(sid):04d}"
 
    def batch_id(self, bid):
     return f"BAT-{int(bid):04d}"        