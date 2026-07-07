"""
ui/pages/batches.py

Phase 2 — Batches module. Lists batches and lets the admin click one to
see its enrolled students side by side.

NOTE: there's no dedicated "students by batch" query in the frozen
backend, so the right-hand panel filters the already-fetched
Students.display_all_students() list client-side by batch_id (which
that method already returns per row). Fine at ~800 students; a
dedicated Students.get_by_batch(batch_id) would be more efficient at
much larger scale, but that's a backend change and the backend stays
frozen for this phase.
"""

from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk

from ui.theme import COLORS, FONTS
from ui.components.batch_form_dialog import BatchFormDialog
from batch import Batch
from student import Students

BATCH_COLUMNS = ("batch_id", "batch_name", "start_time", "end_time", "classroom")
BATCH_HEADINGS = {
    "batch_id": "ID", "batch_name": "Batch", "start_time": "Start",
    "end_time": "End", "classroom": "Room",
}

STUDENT_COLUMNS = ("student_id", "full_name", "phone", "status")
STUDENT_HEADINGS = {
    "student_id": "ID", "full_name": "Name", "phone": "Phone", "status": "Status",
}


class BatchesPage(ctk.CTkFrame):

    def __init__(self, master, admin_info):
        super().__init__(master, fg_color="transparent")

        self.admin_info = admin_info

        self.batch_backend = Batch()
        self.students_backend = Students()

        self.selected_batch_id = None
        self.selected_batch_name = None

        self._build_ui()
        self._refresh_batches()

    def _build_ui(self):

        # ==========================
        # Header
        # ==========================

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0,20))

        ctk.CTkLabel(
            header,
            text="Batch Management",
            font=FONTS["h1"],
            text_color=COLORS["text_primary"]
        ).pack(side="left")

        # ==========================
        # Toolbar
        # ==========================

        toolbar = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        toolbar.pack(fill="x", pady=(0,15))

        self.search_entry = ctk.CTkEntry(
            toolbar,
            width=250,
            placeholder_text="Search batch..."
        )

        self.search_entry.pack(side="left")
        self.search_entry.bind(
            "<KeyRelease>",
            lambda e: self._search_batch()
        )

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            width=110,
            command=self._refresh_batches
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            toolbar,
            text="+ Add Batch",
            width=140,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self._open_add_dialog
        ).pack(side="right")

        # ==========================
        # Main Body
        # ==========================

        self._style_treeview()

        body = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        body.pack(
            fill="both",
            expand=True
        )

        body.grid_columnconfigure(
            0,
            weight=1
        )

        body.grid_columnconfigure(
            1,
            weight=1
        )

        body.grid_rowconfigure(
            0,
            weight=1
        )

        # ==========================
        # LEFT PANEL
        # ==========================

        left = ctk.CTkFrame(
            body,
            fg_color=COLORS["bg_surface"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )

        left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,8)
        )

        ctk.CTkLabel(
            left,
            text="All Batches",
            font=FONTS["h3"],
            text_color=COLORS["text_primary"]
        ).pack(
            anchor="w",
            padx=15,
            pady=(15,8)
        )

        table_frame = ctk.CTkFrame(
            left,
            fg_color="transparent"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        self.batch_tree = ttk.Treeview(
            table_frame,
            columns=BATCH_COLUMNS,
            show="headings",
            style="Dark.Treeview"
        )

        for col in BATCH_COLUMNS:

            self.batch_tree.heading(
                col,
                text=BATCH_HEADINGS[col]
            )

            self.batch_tree.column(
                col,
                width=120,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.batch_tree.yview
        )

        self.batch_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.batch_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.batch_tree.bind(
            "<<TreeviewSelect>>",
            lambda e: self._on_batch_selected()
        )

        self.batch_tree.bind(
            "<Double-1>",
            lambda e: self._edit_batch()
        )

        # ==========================
        # LEFT BUTTONS
        # ==========================

        buttons = ctk.CTkFrame(
            left,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkButton(
            buttons,
            text="Edit",
            command=self._edit_batch
        ).pack(
            side="left",
            padx=4
        )

        ctk.CTkButton(
            buttons,
            text="Delete",
            fg_color=COLORS["error"],
            hover_color="#9d2020",
            command=self._delete_batch
        ).pack(
            side="left",
            padx=4
        )

        # ==========================
        # RIGHT PANEL
        # ==========================

        right = ctk.CTkFrame(
            body,
            fg_color=COLORS["bg_surface"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )

        right.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8,0)
        )

        self.right_title = ctk.CTkLabel(
            right,
            text="Students in Batch",
            font=FONTS["h3"],
            text_color=COLORS["text_primary"]
        )

        self.right_title.pack(
            anchor="w",
            padx=15,
            pady=(15,8)
        )

        self.student_tree = ttk.Treeview(
            right,
            columns=STUDENT_COLUMNS,
            show="headings",
            style="Dark.Treeview"
        )

        for col in STUDENT_COLUMNS:

            self.student_tree.heading(
                col,
                text=STUDENT_HEADINGS[col]
            )

            self.student_tree.column(
                col,
                width=120,
                anchor="center"
            )

        self.student_tree.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

    def _style_treeview(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Dark.Treeview",
            background=COLORS["bg_surface"], fieldbackground=COLORS["bg_surface"],
            foreground=COLORS["text_primary"], rowheight=30, borderwidth=0,
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

    def _refresh_batches(self):

     self.batch_tree.delete(*self.batch_tree.get_children())

     try:
         rows = self.batch_backend.display_all_batches()

         for row in rows:
             self.batch_tree.insert("", "end", iid=str(row[0]), values=row)

     except Exception as e:
        print(e)

     self.student_tree.delete(*self.student_tree.get_children())

     self.right_title.configure(
        text="Students in Batch"
    )

     self.selected_batch_id = None
     self.selected_batch_name = None


    def _search_batch(self):

     keyword = self.search_entry.get().strip()

     self.batch_tree.delete(*self.batch_tree.get_children())

     if keyword == "":
         rows = self.batch_backend.display_all_batches()
     else:
         rows = self.batch_backend.search_batch(keyword)

     for row in rows:
        self.batch_tree.insert(
            "",
            "end",
            iid=str(row[0]),
            values=row
        )

    def _on_batch_selected(self):

     selection = self.batch_tree.selection()

     if not selection:
        return

     batch = self.batch_tree.item(selection[0])["values"]

     self.selected_batch_id = batch[0]
     self.selected_batch_name = batch[1]

     self.right_title.configure(
        text=f"Students - {self.selected_batch_name}"
    )

     self.student_tree.delete(*self.student_tree.get_children())

     try:

        students = self.batch_backend.get_students_by_batch(
            self.selected_batch_id
        )

        for student in students:

            self.student_tree.insert(
                "",
                "end",
                values=student
            )

     except Exception as e:
         print(e)

    def _open_add_dialog(self):

     BatchFormDialog(
        self,
        on_saved=self._refresh_batches
    )

    def _edit_batch(self):

     if self.selected_batch_id is None:
        return

     batch = self.batch_backend.get_batch_details(
        self.selected_batch_id
    )

     BatchFormDialog(
        self,
        on_saved=self._refresh_batches,
        batch_data=batch
    )
    def _delete_batch(self):

        if self.selected_batch_id is None:
            return

        answer = messagebox.askyesno(
            "Delete Batch",
            "Delete this batch?"
        )

        if not answer:
            return

        try:
            self.batch_backend.delete_batch(self.selected_batch_id)
            self._refresh_batches()
        except Exception as e:
            messagebox.showerror("Error", str(e))