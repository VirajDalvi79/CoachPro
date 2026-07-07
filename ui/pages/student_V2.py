from tkinter import ttk
import customtkinter as ctk

from ui.theme import COLORS, FONTS
from ui.components.dialogs import ConfirmDialog, show_success, show_error
from ui.components.student_form_dialog import StudentFormDialog
from student import Students
from batch import Batch
import os
from id_card_generator import generate_student_id_card

COLUMNS = ("student_id", "full_name", "phone", "batch", "status")


class StudentsPageV2(ctk.CTkFrame):

    def __init__(self, master, admin_info=None):
        super().__init__(master, fg_color="transparent")

        self.students_backend = Students()
        self.batch_backend = Batch()

        self._build_ui()
        self._refresh()

    def _build_ui(self):

        self._style_treeview()



        # ---------- Header ----------

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            header,
            text="Students",
            font=FONTS["h1"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="+ Add Student",
            width=150,
            height=38,
            corner_radius=10,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self._open_add_dialog,
        ).pack(side="right")

        # ---------- Stat Cards ----------

        stats = ctk.CTkFrame(self, fg_color="transparent")
        stats.pack(fill="x", pady=(0, 18))

        for i in range(3):
            stats.grid_columnconfigure(i, weight=1)

        self.total_card = self._stat_card(stats, "Total Students", "0", 0)
        self.active_card = self._stat_card(stats, "Active", "0", 1)
        self.inactive_card = self._stat_card(stats, "Inactive", "0", 2)

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
            placeholder_text="Search by name, phone, ID...",
            width=360,
            height=38,
            corner_radius=10,
        )
        self.search_entry.pack(side="left", padx=14, pady=12)
        self.search_entry.bind("<Return>", lambda e: self._search())

        ctk.CTkButton(
            toolbar,
            text="Search",
            width=100,
            height=36,
            corner_radius=10,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["border"],
            command=self._search,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            width=100,
            height=36,
            corner_radius=10,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["border"],
            command=self._refresh,
        ).pack(side="left")

        # ---------- Table ----------

        table_card = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_surface"],
            corner_radius=14,
            border_width=1,
            border_color=COLORS["border"],
        )
        table_card.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_card,
            columns=COLUMNS,
            show="headings",
            style="Students.Treeview",
        )

        headings = {
            "student_id": "Student ID",
            "full_name": "Student Name",
            "phone": "Phone",
            "batch": "Batch",
            "status": "Status",
        }

        for col in COLUMNS:
            self.tree.heading(col, text=headings[col])

        self.tree.column("student_id", width=120, anchor="center")
        self.tree.column("full_name", width=240, anchor="w")
        self.tree.column("phone", width=150, anchor="center")
        self.tree.column("batch", width=180, anchor="w")
        self.tree.column("status", width=110, anchor="center")

        vsb = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(1, 0), pady=1)
        vsb.pack(side="right", fill="y")

        self.empty_label = ctk.CTkLabel(
    table_card,
    text="👨‍🎓\n\nNo students found.\n\nClick '+ Add Student' to begin.",
    font=FONTS["body"],
    text_color=COLORS["text_secondary"],
    justify="center",
)

        self.tree.bind("<Double-1>", lambda e: self._open_details())

        # ---------- Actions ----------

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", pady=(12, 0))

        ctk.CTkButton(
            actions,
            text="View Details",
            width=130,
            height=36,
            corner_radius=10,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["border"],
            command=self._open_details,
        ).pack(side="left")

        ctk.CTkButton(
            actions,
            text="Edit",
            width=100,
            height=36,
            corner_radius=10,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["border"],
            command=self._open_edit_dialog,
        ).pack(side="left", padx=8)
        
        ctk.CTkButton(
    actions,
    text="Generate ID Card",
    width=160,
    height=36,
    corner_radius=10,
    fg_color=COLORS["bg_surface_alt"],
    hover_color=COLORS["border"],
    command=self.generate_id_card,
).pack(side="left", padx=8)
        
        ctk.CTkButton(
            actions,
            text="Deactivate",
            width=120,
            height=36,
            corner_radius=10,
            fg_color="transparent",
            hover_color=COLORS["error"],
            text_color=COLORS["text_secondary"],
            command=self._confirm_deactivate,
        ).pack(side="left")

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
            "Students.Treeview",
            background=COLORS["bg_surface"],
            fieldbackground=COLORS["bg_surface"],
            foreground=COLORS["text_primary"],
            rowheight=38,
            borderwidth=0,
            font=FONTS["body"],
        )

        style.configure(
            "Students.Treeview.Heading",
            background=COLORS["bg_surface_alt"],
            foreground=COLORS["text_secondary"],
            borderwidth=0,
            font=FONTS["small"],
        )

        style.map(
            "Students.Treeview",
            background=[("selected", COLORS["accent_soft"])],
            foreground=[("selected", COLORS["text_primary"])],
        )

    def _batch_name_lookup(self):

        return {
            batch[0]: batch[1]
            for batch in self.batch_backend.display_all_batches()
        }

    def _format_student_id(self, student_id):

        return f"STU-{int(student_id):04d}"

    def _populate(self, rows):

     self.tree.delete(*self.tree.get_children())

     batch_names = self._batch_name_lookup()

     total = len(rows)
     active = 0
     inactive = 0

     for row in rows:

        student_id, full_name, phone, batch_id, status = row

        if status == "Active":
            active += 1
            status_display = "● Active"
        else:
            inactive += 1
            status_display = "● Inactive"

        batch_name = batch_names.get(batch_id, "—")

        self.tree.insert(
            "",
            "end",
            iid=str(student_id),
            values=(
                self._format_student_id(student_id),
                full_name.title(),
                phone or "—",
                batch_name,
                status_display,
            ),
        )

     if not rows:
        self.empty_label.place(relx=0.5, rely=0.5, anchor="center")
     else:
        self.empty_label.place_forget()

     self.total_card.configure(text=str(total))
     self.active_card.configure(text=str(active))
     self.inactive_card.configure(text=str(inactive))

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

        StudentFormDialog(
            self,
            on_saved=self._refresh,
        )

    def _open_edit_dialog(self):

        student_id = self._selected_student_id()

        if student_id is None:
            show_error(
                self,
                "Select a student first."
            )
            return

        StudentFormDialog(
            self,
            on_saved=self._refresh,
            student_id=student_id,
        )

    def _open_details(self):

        student_id = self._selected_student_id()

        if student_id is None:
            show_error(
                self,
                "Select a student first."
            )
            return

        StudentFormDialog(
            self,
            on_saved=self._refresh,
            student_id=student_id,
        )

    def _confirm_deactivate(self):

        student_id = self._selected_student_id()

        if student_id is None:
            show_error(
                self,
                "Select a student first."
            )
            return

        ConfirmDialog(
            self,
            title="Deactivate Student",
            message=(
                "This marks the student as Inactive. "
                "Attendance, marks, and fee history are kept. Continue?"
            ),
            on_confirm=lambda: self._deactivate(student_id),
            confirm_text="Deactivate",
            danger=True,
        )

    def _deactivate(self, student_id):

        self.students_backend.deactivate_student(student_id)

        show_success(
            self,
            "Student deactivated."
        )

        self._refresh()


    def generate_id_card(self):

     student_id = self._selected_student_id()

     if student_id is None:
        show_error(
            self,
            "Select a student first."
        )
        return

     try:
        student = self.students_backend.get_student_details(student_id)

        # Adjust indexes if your student table order is different.
        (
            _,
            full_name,
            phone,
            father_name,
            mother_name,
            parent_phone,
            batch_id,
            admission_date,
            status,
            remarks,
            total_fee,
        ) = student

        batch_names = self._batch_name_lookup()
        batch_name = batch_names.get(batch_id, "—")

        os.makedirs("id_cards", exist_ok=True)

        file_path = os.path.join(
            "id_cards",
            f"id_card_STU-{student_id:04d}.pdf"
        )

        generate_student_id_card(
            file_path=file_path,
            student_id=student_id,
            student_name=full_name,
            phone=phone,
            parent_phone=parent_phone,
            batch_name=batch_name,
        )

        show_success(
            self,
            f"ID card generated:\n{file_path}"
        )

     except Exception as e:
        show_error(
            self,
            "ID Card Error",
            str(e)
        )    