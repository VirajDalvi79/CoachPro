from tkinter import ttk, messagebox
import customtkinter as ctk

from ui.theme import COLORS, FONTS
from ui.components.batch_form_dialog import BatchFormDialog
from batch import Batch
from ui.components.dialogs import ConfirmDialog, show_success, show_error

def show_error(parent, title_or_message, message=None):
    if message is None:
        title = "Error"
        message = title_or_message
    else:
        title = title_or_message

    messagebox.showerror(title, message, parent=parent)


def show_success(parent, message, title="Success"):
    messagebox.showinfo(title, message, parent=parent)


BATCH_COLUMNS = ("batch_id", "batch_name", "time", "classroom")
STUDENT_COLUMNS = ("student_id", "full_name", "phone", "status")


class BatchesPageV2(ctk.CTkFrame):

    def __init__(self, master, admin_info=None):
        super().__init__(master, fg_color="transparent")

        self.batch_backend = Batch()

        self.selected_batch_id = None
        self.selected_batch_name = None

        self._build_ui()
        self._refresh_batches()

    def _build_ui(self):

        self._style_treeview()

        # ---------- Header ----------

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            header,
            text="Batches",
            font=FONTS["h1"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="+ Add Batch",
            width=150,
            height=38,
            corner_radius=10,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self._open_add_dialog,
        ).pack(side="right")

        # ---------- Stats ----------

        stats = ctk.CTkFrame(self, fg_color="transparent")
        stats.pack(fill="x", pady=(0, 18))

        stats.grid_columnconfigure(0, weight=1)
        stats.grid_columnconfigure(1, weight=1)

        self.total_batches_card = self._stat_card(
            stats,
            "Total Batches",
            "0",
            0,
        )

        self.assigned_students_card = self._stat_card(
            stats,
            "Students Assigned",
            "0",
            1,
        )

        # ---------- Toolbar ----------

        toolbar = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_surface"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )
        toolbar.pack(fill="x", pady=(0, 14))

        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search batch name or classroom...",
            width=360,
            height=38,
            corner_radius=10,
        )
        self.search_entry.pack(side="left", padx=14, pady=12)
        self.search_entry.bind("<Return>", lambda e: self._search_batches())

        ctk.CTkButton(
            toolbar,
            text="Search",
            width=100,
            height=36,
            corner_radius=10,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["border"],
            command=self._search_batches,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            width=100,
            height=36,
            corner_radius=10,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["border"],
            command=self._refresh_batches,
        ).pack(side="left")

        # ---------- Main Body ----------

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True)

        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        # Left panel

        left = ctk.CTkFrame(
            body,
            fg_color=COLORS["bg_surface"],
            corner_radius=14,
            border_width=1,
            border_color=COLORS["border"],
        )
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(
            left,
            text="All Batches",
            font=FONTS["h2"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=18, pady=(16, 10))

        self.batch_tree = ttk.Treeview(
            left,
            columns=BATCH_COLUMNS,
            show="headings",
            style="Batches.Treeview",
        )

        headings = {
            "batch_id": "Batch ID",
            "batch_name": "Batch Name",
            "time": "Time",
            "classroom": "Room",
        }

        for col in BATCH_COLUMNS:
            self.batch_tree.heading(col, text=headings[col])

        self.batch_tree.column("batch_id", width=110, anchor="center")
        self.batch_tree.column("batch_name", width=200, anchor="w")
        self.batch_tree.column("time", width=170, anchor="center")
        self.batch_tree.column("classroom", width=100, anchor="center")

        self.batch_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.batch_tree.bind("<<TreeviewSelect>>", lambda e: self._on_batch_selected())
        self.batch_tree.bind("<Double-1>", lambda e: self._edit_batch())

        batch_actions = ctk.CTkFrame(left, fg_color="transparent")
        batch_actions.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkButton(
            batch_actions,
            text="Edit",
            width=90,
            command=self._edit_batch,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            batch_actions,
            text="Delete",
            width=90,
            fg_color=COLORS["error"],
            command=self._delete_batch,
        ).pack(side="left", padx=5)

        # Right panel

        right = ctk.CTkFrame(
            body,
            fg_color=COLORS["bg_surface"],
            corner_radius=14,
            border_width=1,
            border_color=COLORS["border"],
        )
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.students_title = ctk.CTkLabel(
            right,
            text="Students in selected batch",
            font=FONTS["h2"],
            text_color=COLORS["text_primary"],
        )
        self.students_title.pack(anchor="w", padx=18, pady=(16, 10))

        self.student_tree = ttk.Treeview(
            right,
            columns=STUDENT_COLUMNS,
            show="headings",
            style="Batches.Treeview",
        )

        student_headings = {
            "student_id": "Student ID",
            "full_name": "Name",
            "phone": "Phone",
            "status": "Status",
        }

        for col in STUDENT_COLUMNS:
            self.student_tree.heading(col, text=student_headings[col])

        self.student_tree.column("student_id", width=110, anchor="center")
        self.student_tree.column("full_name", width=220, anchor="w")
        self.student_tree.column("phone", width=150, anchor="center")
        self.student_tree.column("status", width=100, anchor="center")

        self.student_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def _stat_card(self, parent, title, value, column):

        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_surface"],
            corner_radius=14,
            border_width=1,
            border_color=COLORS["border"],
        )
        card.grid(row=0, column=column, sticky="nsew", padx=8)

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=FONTS["h1"],
            text_color=COLORS["text_primary"],
        )
        value_label.pack(anchor="w", padx=18, pady=(15, 2))

        ctk.CTkLabel(
            card,
            text=title,
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=18, pady=(0, 15))

        return value_label
    
    def _style_treeview(self):

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Batches.Treeview",
            background=COLORS["bg_surface"],
            fieldbackground=COLORS["bg_surface"],
            foreground=COLORS["text_primary"],
            rowheight=38,
            borderwidth=0,
            font=FONTS["body"],
        )

        style.configure(
            "Batches.Treeview.Heading",
            background=COLORS["bg_surface_alt"],
            foreground=COLORS["text_secondary"],
            borderwidth=0,
            font=FONTS["small"],
        )

        style.map(
            "Batches.Treeview",
            background=[("selected", COLORS["accent_soft"])],
            foreground=[("selected", COLORS["text_primary"])],
        )

    def _format_batch_id(self, batch_id):
        return f"BAT-{int(batch_id):04d}"

    def _format_student_id(self, student_id):
        return f"STU-{int(student_id):04d}"

    def _format_time(self, start_time, end_time):
        return f"{str(start_time)[:5]} - {str(end_time)[:5]}"

    def _refresh_batches(self):

        self.search_entry.delete(0, "end")

        rows = self.batch_backend.display_all_batches()

        self._populate_batches(rows)

    def _search_batches(self):

        keyword = self.search_entry.get().strip()

        if not keyword:
            self._refresh_batches()
            return

        rows = self.batch_backend.search_batch(keyword)

        self._populate_batches(rows)

    def _populate_batches(self, rows):

        self.batch_tree.delete(*self.batch_tree.get_children())
        self.student_tree.delete(*self.student_tree.get_children())

        self.selected_batch_id = None
        self.selected_batch_name = None

        assigned_count = 0

        for row in rows:

            batch_id, batch_name, start_time, end_time, classroom = row

            students = self.batch_backend.get_students_by_batch(batch_id)
            assigned_count += len(students)

            self.batch_tree.insert(
                "",
                "end",
                iid=str(batch_id),
                values=(
                    self._format_batch_id(batch_id),
                    batch_name,
                    self._format_time(start_time, end_time),
                    classroom or "—",
                ),
            )

        self.total_batches_card.configure(text=str(len(rows)))
        self.assigned_students_card.configure(text=str(assigned_count))

        self.students_title.configure(
            text="Students in selected batch"
        )

    def _on_batch_selected(self):

        selection = self.batch_tree.selection()

        if not selection:
            return

        batch_id = int(selection[0])
        values = self.batch_tree.item(selection[0])["values"]

        self.selected_batch_id = batch_id
        self.selected_batch_name = values[1]

        self.students_title.configure(
            text=f"Students in {self.selected_batch_name}"
        )

        self._load_students_for_batch(batch_id)

    def _load_students_for_batch(self, batch_id):

        self.student_tree.delete(*self.student_tree.get_children())

        try:
            students = self.batch_backend.get_students_by_batch(batch_id)

            for student_id, full_name, phone, status in students:

                status_display = (
                    "● Active"
                    if status == "Active"
                    else "● Inactive"
                )

                self.student_tree.insert(
                    "",
                    "end",
                    iid=str(student_id),
                    values=(
                        self._format_student_id(student_id),
                        full_name.title(),
                        phone or "—",
                        status_display,
                    ),
                )

        except Exception as e:
                show_error(
                self,
                "Error",
                str(e)
            )

    def _open_add_dialog(self):

            BatchFormDialog(
            self,
            on_saved=self._refresh_batches,
        )

    def _edit_batch(self):

        if self.selected_batch_id is None:
            show_error(
                self,
                "Select a batch first."
            )
            return

        batch = self.batch_backend.get_batch_details(
            self.selected_batch_id
        )

        BatchFormDialog(
            self,
            on_saved=self._refresh_batches,
            batch_data=batch,
        )

    def _delete_batch(self):

        if self.selected_batch_id is None:
            show_error(
                self,
                "Select a batch first."
            )
            return
  
        ConfirmDialog(
            self,
    title="Delete Batch",
    message="This will delete the selected batch. Continue?",
    on_confirm=lambda: self._delete_selected_batch(),
    confirm_text="Delete",
    danger=True,
)
    def _delete_selected_batch(self):

     try:
        self.batch_backend.delete_batch(self.selected_batch_id)

        show_success(
            self,
            "Batch deleted."
        )

        self._refresh_batches()

     except Exception as e:
        show_error(
            self,
            "Error",
            str(e)
        )    
        
