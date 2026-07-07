import datetime
import customtkinter as ctk
from tkinter import ttk

from ui.theme import COLORS, FONTS
from student import Students
from attendance import Attendance
from reports import ReportsBackend
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from settings_manager import SettingsManager

class StatCard(ctk.CTkFrame):
    def __init__(self, master, title, value, subtitle="", icon=""):
        super().__init__(
            master,
            fg_color=COLORS["bg_surface"],
            corner_radius=14,
            border_width=1,
            border_color=COLORS["border"],
        )

        ctk.CTkLabel(
            self,
            text=icon,
            font=FONTS["h2"],
            text_color=COLORS["accent"],
        ).pack(anchor="w", padx=18, pady=(16, 4))

        ctk.CTkLabel(
            self,
            text=str(value),
            font=FONTS["h1"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=18)

        ctk.CTkLabel(
            self,
            text=title,
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=18, pady=(2, 2))

        ctk.CTkLabel(
            self,
            text=subtitle,
            font=FONTS["small"],
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=18, pady=(0, 16))


class DashboardPage(ctk.CTkFrame):

    def __init__(self, master, admin_info):
        super().__init__(master, fg_color="transparent")

        self.admin_info = admin_info
        self.students_backend = Students()
        self.attendance_backend = Attendance()
        self.reports_backend = ReportsBackend()
        self.settings_manager = SettingsManager()
        self.settings = self.settings_manager.load_settings()
        self._build_ui()
        self.load_dashboard()

    def _build_ui(self):
        self._style_treeview()

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.scroll.pack(fill="both", expand=True)

    # ---------- HEADER ----------

        header = ctk.CTkFrame(self.scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
        left,
        text=f"Welcome back, {self.admin_info.get('full_name', 'Admin')}",
        font=FONTS["h1"],
        text_color=COLORS["text_primary"],
    ).pack(anchor="w")
        
        ctk.CTkLabel(
    left,
    text=self.settings.get("institute_name", "CoachPro Academy"),
    font=FONTS["h2"],
    text_color=COLORS["accent"],
).pack(anchor="w", pady=(4, 0))
        
        ctk.CTkLabel(
        left,
        text=datetime.date.today().strftime("%A, %d %B %Y"),
        font=FONTS["body"],
        text_color=COLORS["text_secondary"],
    ).pack(anchor="w", pady=(4, 0))

        ctk.CTkButton(
        header,
        text="Refresh",
        width=120,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        command=self.load_dashboard,
    ).pack(side="right", pady=8)

    # ---------- STAT CARDS ----------

        self.cards_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.cards_frame.pack(fill="x")

        for i in range(4):
         self.cards_frame.grid_columnconfigure(i, weight=1)

    # ---------- QUICK ACTIONS ----------

        quick = ctk.CTkFrame(
        self.scroll,
        fg_color=COLORS["bg_surface"],
        corner_radius=14,
        border_width=1,
        border_color=COLORS["border"],
    )
        quick.pack(fill="x", pady=24)

        ctk.CTkLabel(
        quick,
        text="Quick Actions",
        font=FONTS["h2"],
        text_color=COLORS["text_primary"],
    ).pack(anchor="w", padx=18, pady=(16, 10))

        actions = ctk.CTkFrame(quick, fg_color="transparent")
        actions.pack(fill="x", padx=18, pady=(0, 18))

        self._action_button(actions, "+ Add Student", "students")
        self._action_button(actions, "+ Add Batch", "batches")
        self._action_button(actions, "Mark Attendance", "attendance")
        self._action_button(actions, "Record Payment", "fees")
        self._action_button(actions, "Marks", "marks")
        self._action_button(actions, "Reports", "reports")

    # ---------- LOWER SECTIONS ----------

        lower = ctk.CTkFrame(self.scroll, fg_color="transparent")
        lower.pack(fill="x")

        lower.grid_columnconfigure(0, weight=1)
        lower.grid_columnconfigure(1, weight=1)

        payments_box = ctk.CTkFrame(
        lower,
        fg_color=COLORS["bg_surface"],
        corner_radius=14,
        border_width=1,
        border_color=COLORS["border"],
    )
        payments_box.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(
        payments_box,
        text="Recent Payments",
        font=FONTS["h2"],
        text_color=COLORS["text_primary"],
    ).pack(anchor="w", padx=18, pady=(16, 10))

        self.payments_tree = ttk.Treeview(
        payments_box,
        columns=("student", "amount", "date"),
        show="headings",
        height=8,
        style="Dashboard.Treeview",
    )

        self.payments_tree.heading("student", text="Student")
        self.payments_tree.heading("amount", text="Amount")
        self.payments_tree.heading("date", text="Date")

        self.payments_tree.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=(0, 18)
    )

        activity_box = ctk.CTkFrame(
        lower,
        fg_color=COLORS["bg_surface"],
        corner_radius=14,
        border_width=1,
        border_color=COLORS["border"],
    )
        activity_box.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(
        activity_box,
        text="Today’s Overview",
        font=FONTS["h2"],
        text_color=COLORS["text_primary"],
    ).pack(anchor="w", padx=18, pady=(16, 10))

        self.defaulters_label = ctk.CTkLabel(
        activity_box,
        text="",
        font=FONTS["body"],
        text_color=COLORS["text_secondary"],
        justify="left",
    )
        self.defaulters_label.pack(anchor="w", padx=18, pady=(10, 18))

        self.overview_label = ctk.CTkLabel(
        activity_box,
        text="Loading...",
        font=FONTS["body"],
        text_color=COLORS["text_secondary"],
        justify="left",
    )
        self.overview_label.pack(anchor="w", padx=18, pady=(0, 18))

    # ---------- CHART SECTION ----------

        chart_box = ctk.CTkFrame(
        self.scroll,
        fg_color=COLORS["bg_surface"],
        corner_radius=14,
        border_width=1,
        border_color=COLORS["border"],
    )
        chart_box.pack(fill="x", pady=(20, 0))

        ctk.CTkLabel(
        chart_box,
        text="Monthly Fee Collection",
        font=FONTS["h2"],
        text_color=COLORS["text_primary"],
    ).pack(anchor="w", padx=18, pady=(16, 8))

        self.chart_container = ctk.CTkFrame(
    chart_box,
    fg_color="transparent",
    height=320,
)
        self.chart_container.pack(fill="x", padx=18, pady=(0, 18))
        self.chart_container.pack_propagate(False)

    def _action_button(self, parent, text, page_key):
        ctk.CTkButton(
            parent,
            text=text,
            width=145,
            height=38,
            corner_radius=10,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["accent"],
            text_color=COLORS["text_primary"],
            command=lambda: self._navigate(page_key),
        ).pack(side="left", padx=(0, 10))

    def _navigate(self, page_key):
        app = self.master.master
        if hasattr(app, "sidebar"):
            app.sidebar._select(page_key)

    def money(self, amount):
        return f"₹{float(amount):,.0f}"

    def load_dashboard(self):

        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        students = self.students_backend.display_all_students()
        active_students = [s for s in students if s[4] == "Active"]

        today = datetime.date.today()
        attendance_rows = self.attendance_backend.get_attendance_by_date(today)

        total_marked = len(attendance_rows)
        present = len([r for r in attendance_rows if r[-1] == "PRESENT"])

        total_fee, collected, pending = self.reports_backend.fees_summary()

        cards = [
            ("Students", len(active_students), "Active enrollments", "👨‍🎓"),
            (
                "Today’s Attendance",
                f"{present}/{total_marked}" if total_marked else "Not Marked",
                "Present / Marked today",
                "📅",
            ),
            ("Collected Fees", self.money(collected), "Total received", "💰"),
            ("Pending Fees", self.money(pending), "Remaining balance", "⚠️"),
        ]

        try:
            defaulters = self.reports_backend.fee_defaulters(5)

            if defaulters:
                lines = ["\nPending Fee Students:"]
                for name, total_fee, paid, pending in defaulters:
                    lines.append(f"• {name} — {self.money(pending)} pending")

                self.defaulters_label.configure(
                    text="\n".join(lines)
                )
            else:
                self.defaulters_label.configure(
                    text="\nNo pending fees 🎉"
                )

        except Exception as e:
            self.defaulters_label.configure(
                text=f"\nCould not load defaulters: {e}"
            )

        for i, (title, value, subtitle, icon) in enumerate(cards):
            StatCard(
                self.cards_frame,
                title,
                value,
                subtitle,
                icon,
            ).grid(row=0, column=i, sticky="nsew", padx=8)

        self.payments_tree.delete(*self.payments_tree.get_children())

        try:
            payments = self.reports_backend.recent_payments(8)
            for student, amount, payment_date, remarks in payments:
                self.payments_tree.insert(
                    "",
                    "end",
                    values=(student, self.money(amount), payment_date),
                )
        except Exception:
            pass

        overview = (
            f"Active Students: {len(active_students)}\n\n"
            f"Attendance Marked Today: {total_marked}\n"
            f"Present Today: {present}\n"
            f"Absent Today: {max(total_marked - present, 0)}\n\n"
            f"Total Fee Value: {self.money(total_fee)}\n"
            f"Collected: {self.money(collected)}\n"
            f"Pending: {self.money(pending)}"
        )

        self.overview_label.configure(text=overview)
        self.load_collection_chart()

    def load_collection_chart(self):

     for widget in self.chart_container.winfo_children():
        widget.destroy()

     rows = self.reports_backend.monthly_collection()

     if not rows:
        ctk.CTkLabel(
            self.chart_container,
            text="No payment data available yet.",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
        ).pack(pady=20)
        return

     months = [str(row[0]) for row in rows]
     totals = [float(row[1]) for row in rows]

     fig = Figure(figsize=(9, 3.2), dpi=100)
     fig.patch.set_facecolor(COLORS["bg_surface"])

     ax = fig.add_subplot(111)
     ax.set_facecolor(COLORS["bg_surface"])

     ax.plot(
        months,
        totals,
        marker="o",
        linewidth=2.8,
    )

     ax.fill_between(
        months,
        totals,
        alpha=0.18,
    )

     ax.set_title(
        "Monthly Fee Collection",
        fontsize=13,
        fontweight="bold",
        color=COLORS["text_primary"],
        pad=14,
    )

     ax.set_ylabel(
        "Amount collected",
        color=COLORS["text_secondary"],
        fontsize=10,
    )

     ax.tick_params(
        axis="x",
        colors=COLORS["text_secondary"],
        labelrotation=25,
    )

     ax.tick_params(
        axis="y",
        colors=COLORS["text_secondary"],
    )

     ax.grid(
        True,
        axis="y",
        alpha=0.18,
    )

     for spine in ax.spines.values():
        spine.set_visible(False)

     ax.yaxis.set_major_formatter(
        lambda value, pos: f"₹{value:,.0f}"
    )

     fig.tight_layout()

     canvas = FigureCanvasTkAgg(
        fig,
        master=self.chart_container,
    )

     canvas.draw()

     canvas.get_tk_widget().pack(
        fill="both",
        expand=True,
    )

    def _style_treeview(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Dashboard.Treeview",
            background=COLORS["bg_surface"],
            foreground=COLORS["text_primary"],
            fieldbackground=COLORS["bg_surface"],
            rowheight=30,
            borderwidth=0,
            font=FONTS["body"],
        )

        style.configure(
            "Dashboard.Treeview.Heading",
            background=COLORS["bg_surface_alt"],
            foreground=COLORS["text_secondary"],
            borderwidth=0,
            font=FONTS["small"],
        )

        style.map(
            "Dashboard.Treeview",
            background=[("selected", COLORS["accent"])],
            foreground=[("selected", COLORS["text_primary"])],
        )