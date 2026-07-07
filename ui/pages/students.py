"""
ui/pages/students.py

Phase 2 — Students module. Search + refresh a scrollable table, and
open dialogs for Add / Edit / View Details / Deactivate — no separate
windows, per the Navigation Philosophy doc.
"""

from tkinter import ttk
import customtkinter as ctk

from ui.theme import COLORS, FONTS
from ui.components.dialogs import ConfirmDialog, show_success, show_error
from ui.components.student_form_dialog import StudentFormDialog
from student import Students
from batch import Batch

COLUMNS = ("student_id", "full_name", "phone", "batch", "status")
HEADINGS = {
    "student_id": "ID", "full_name": "Name", "phone": "Phone",
    "batch": "Batch", "status": "Status",
}


class StudentsPage(ctk.CTkFrame):
    def __init__(self, master, admin_info):
        super().__init__(master, fg_color="transparent")
        self.students_backend = Students()
        self.batch_backend = Batch()

        self._build_ui()
        self._refresh()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            header, text="Students", font=FONTS["h1"], text_color=COLORS["text_primary"]
        ).pack(side="left")

        ctk.CTkButton(
            header, text="+ Add Student", width=150, height=38, corner_radius=8,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=self._open_add_dialog
        ).pack(side="right")

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 16))

        self.search_entry = ctk.CTkEntry(
            toolbar, placeholder_text="Search by name, phone, ID...", width=320,
            height=36, corner_radius=8
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<Return>", lambda e: self._search())

        ctk.CTkButton(
            toolbar, text="Search", width=100, height=36, corner_radius=8,
            fg_color=COLORS["bg_surface_alt"], hover_color=COLORS["border"],
            command=self._search
        ).pack(side="left", padx=(8, 0))

        ctk.CTkButton(
            toolbar, text="Refresh", width=100, height=36, corner_radius=8,
            fg_color=COLORS["bg_surface_alt"], hover_color=COLORS["border"],
            command=self._refresh
        ).pack(side="left", padx=(8, 0))

        table_frame = ctk.CTkFrame(
            self, fg_color=COLORS["bg_surface"], corner_radius=12,
            border_width=1, border_color=COLORS["border"]
        )
        table_frame.pack(fill="both", expand=True)

        self._style_treeview()

        self.tree = ttk.Treeview(table_frame, columns=COLUMNS, show="headings", style="Dark.Treeview")
        for col in COLUMNS:

         self.tree.heading(col, text=HEADINGS[col])

         if col == "student_id":

          self.tree.column(
            col,
            width=110,
            anchor="center",
        )

         elif col == "phone":

          self.tree.column(
            col,
            width=150,
            anchor="center",
        )

         elif col == "status":

          self.tree.column(
            col,
            width=100,
            anchor="center",
        )

        else:

         self.tree.column(
            col,
            width=220,
            anchor="w",
        )

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(1, 0), pady=1)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda e: self._open_details())

        action_row = ctk.CTkFrame(self, fg_color="transparent")
        action_row.pack(fill="x", pady=(12, 0))

        ctk.CTkButton(
            action_row, text="View Details", width=130, height=36, corner_radius=8,
            fg_color=COLORS["bg_surface_alt"], hover_color=COLORS["border"],
            command=self._open_details
        ).pack(side="left")

        ctk.CTkButton(
            action_row, text="Edit", width=100, height=36, corner_radius=8,
            fg_color=COLORS["bg_surface_alt"], hover_color=COLORS["border"],
            command=self._open_edit_dialog
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            action_row, text="Deactivate", width=110, height=36, corner_radius=8,
            fg_color="transparent", hover_color=COLORS["error"],
            text_color=COLORS["text_secondary"],
            command=self._confirm_deactivate
        ).pack(side="left")

    def _style_treeview(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Dark.Treeview",
            background=COLORS["bg_surface"], fieldbackground=COLORS["bg_surface"],
            foreground=COLORS["text_primary"], rowheight=32, borderwidth=0,
            font=FONTS["body"],
        )
        style.configure(
            "Dark.Treeview.Heading",
            background=COLORS["bg_surface_alt"], foreground=COLORS["text_secondary"],
            borderwidth=0, font=FONTS["small"],
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", COLORS["accent_soft"])],
            foreground=[("selected", COLORS["text_primary"])],
        )

    def _batch_name_lookup(self):
        return {b[0]: b[1] for b in self.batch_backend.display_all_batches()}

    def _populate(self, rows):

     self.tree.delete(*self.tree.get_children())
 
     batch_names = self._batch_name_lookup()

     for row in rows:

        student_id, full_name, phone, batch_id, status = row

        batch_label = batch_names.get(batch_id, "—")

        display_id = f"STU-{student_id:04d}"

        self.tree.insert(
            "",
            "end",
            iid=str(student_id),
            values=(
                display_id,
                full_name.title(),
                phone or "—",
                batch_label,
                status,
            ),
        )

    def _refresh(self):
        self.search_entry.delete(0, "end")
        rows = self.students_backend.display_all_students()
        self._populate(rows)

    def _search(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            self._refresh()
            return
        rows = self.students_backend.search_student(keyword)
        self._populate(rows)

    def _selected_student_id(self):
        selection = self.tree.selection()
        if not selection:
            return None
        return int(selection[0])

    def _open_add_dialog(self):
        StudentFormDialog(self, on_saved=self._refresh)

    def _open_edit_dialog(self):
        student_id = self._selected_student_id()
        if student_id is None:
            show_error(self, "Select a student first.")
            return
        StudentFormDialog(self, on_saved=self._refresh, student_id=student_id)

    def _open_details(self):
        student_id = self._selected_student_id()
        if student_id is None:
            show_error(self, "Select a student first.")
            return
        StudentFormDialog(self, on_saved=self._refresh, student_id=student_id)

    def _confirm_deactivate(self):
        student_id = self._selected_student_id()
        if student_id is None:
            show_error(self, "Select a student first.")
            return

        ConfirmDialog(
            self, title="Deactivate Student",
            message="This marks the student as Inactive. Attendance, marks, "
                    "and fee history are kept — nothing is deleted. Continue?",
            on_confirm=lambda: self._deactivate(student_id),
            confirm_text="Deactivate", danger=True
        )

    def _deactivate(self, student_id):
        self.students_backend.deactivate_student(student_id)
        show_success(self, "Student deactivated.")
        self._refresh()
