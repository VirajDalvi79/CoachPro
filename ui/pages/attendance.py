import datetime
from tkinter import ttk

import customtkinter as ctk

from ui.theme import COLORS, FONTS
from ui.components.dialogs import show_error, show_success
from attendance import Attendance
from student import Students
from batch import Batch


class AttendancePage(ctk.CTkFrame):

    def __init__(self, master, admin_info=None):
        super().__init__(master, fg_color=COLORS["bg_app"])

        self.admin_info = admin_info

        self.attendance_backend = Attendance()
        self.student_backend = Students()
        self.batch_backend = Batch()
        

        self.batch_map = {}

        self.current_students = []
        self.attendance_vars = {}

        self.build_ui()
        self.load_batches()

    def build_ui(self):

        # ---------------- Header ----------------

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(20, 10))

        ctk.CTkLabel(
            header,
            text="Attendance",
            font=FONTS["h1"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        # ---------------- Controls ----------------

        controls = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_surface"],
            corner_radius=10,
        )
        controls.pack(fill="x", padx=25)

        ctk.CTkLabel(
            controls,
            text="Batch",
            font=FONTS["body"],
        ).grid(row=0, column=0, padx=15, pady=15)

        self.batch_combo = ctk.CTkComboBox(
            controls,
            width=180,
            values=[],
        )
        self.batch_combo.grid(row=0, column=1)

        ctk.CTkLabel(
            controls,
            text="Date",
            font=FONTS["body"],
        ).grid(row=0, column=2, padx=(20, 10))

        self.date_entry = ctk.CTkEntry(
            controls,
            width=140,
        )
        self.date_entry.insert(
            0,
            str(datetime.date.today())
        )
        self.date_entry.grid(row=0, column=3)

        ctk.CTkButton(
            controls,
            text="Load Students",
            command=self.load_students,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
        ).grid(row=0, column=4, padx=15)

        ctk.CTkButton(
            controls,
            text="Save Attendance",
            command=self.save_attendance,
            fg_color="green",
        ).grid(row=0, column=5, padx=10)

        ctk.CTkButton(
            controls,
            text="History",
            command=self.view_history,
        ).grid(row=0, column=6, padx=10)

        # ---------------- Student Count ----------------

        self.count_label = ctk.CTkLabel(
            self,
            text="Students Loaded : 0",
            font=FONTS["body"],
        )
        self.count_label.pack(
            anchor="w",
            padx=30,
            pady=(10, 5),
        )

        # ---------------- Scroll Area ----------------

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
        )
        self.scroll.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20),
        )


        # --------------------------------------------------
    # LOAD BATCHES
    # --------------------------------------------------

    def load_batches(self):

        try:

            batches = self.batch_backend.display_all_batches()

        except Exception as e:

            show_error(
                self,
                "Error",
                str(e)
            )

            return

        self.batch_map.clear()

        names = []

        for batch in batches:

            batch_id = batch[0]
            batch_name = batch[1]

            self.batch_map[batch_name] = batch_id
            names.append(batch_name)

        if not names:

            names = ["No Batches"]

        self.batch_combo.configure(values=names)
        self.batch_combo.set(names[0])

    # --------------------------------------------------
    # LOAD STUDENTS
    # --------------------------------------------------

    def load_students(self):

        # clear previous students

        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.current_students.clear()
        self.attendance_vars.clear()

        batch_name = self.batch_combo.get()

        if batch_name == "No Batches":
            return

        batch_id = self.batch_map[batch_name]

        try:

            students = self.student_backend.display_all_students()

        except Exception as e:

            show_error(
                self,
                "Error",
                str(e)
            )
            return

        loaded = []

        for student in students:

            student_id = student[0]
            full_name = student[1]
            phone = student[2]
            student_batch = student[3]
            status = student[4]

            if student_batch == batch_id and status.lower() == "active":

                loaded.append(student)

        self.current_students = loaded

        self.count_label.configure(
            text=f"Students Loaded : {len(loaded)}"
        )

        if len(loaded) == 0:

            ctk.CTkLabel(
                self.scroll,
                text="No students in this batch.",
                font=FONTS["body"],
            ).pack(pady=30)

            return

        for student in loaded:

            student_id = student[0]
            full_name = student[1]

            card = ctk.CTkFrame(
                self.scroll,
                fg_color=COLORS["bg_surface"],
                corner_radius=10,
            )

            card.pack(
                fill="x",
                padx=5,
                pady=6,
            )

            ctk.CTkLabel(
    card,
    text=f"STU-{int(student_id):04d}   {full_name.title()}",
    font=FONTS["body"],
).pack(
    side="left",
    padx=15,
    pady=15,
)
            var = ctk.StringVar(value="PRESENT")

            present = ctk.CTkRadioButton(
                card,
                text="Present",
                variable=var,
                value="PRESENT",
            )

            present.pack(
                side="right",
                padx=(10,20),
            )

            absent = ctk.CTkRadioButton(
                card,
                text="Absent",
                variable=var,
                value="ABSENT",
            )

            absent.pack(
                side="right",
            )

            self.attendance_vars[student_id] = var

        # --------------------------------------------------
    # SAVE ATTENDANCE
    # --------------------------------------------------

    def save_attendance(self):

        if len(self.current_students) == 0:

            show_error(
                self,
                "Error",
                "Load students first."
            )

            return

        attendance_date = self.date_entry.get()

        try:
            attendance_date = datetime.datetime.strptime(
                attendance_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            show_error(
                self,
                "Error",
                "Date must be YYYY-MM-DD"
            )

            return

        saved = 0

        try:

            # existing attendance for this date
            existing = self.attendance_backend.get_attendance_by_date(
                attendance_date
            )

            already_marked = {
                row[0] for row in existing
            }

            for student in self.current_students:

                student_id = student[0]

                if student_id in already_marked:
                    continue

                status = self.attendance_vars[student_id].get()

                self.attendance_backend.mark_attendance(
                    student_id,
                    attendance_date,
                    status,
                )

                saved += 1

            show_success(
                self,
                f"{saved} attendance records saved."
            )

        except Exception as e:

            show_error(
                self,
                "Error",
                str(e)
            )

    def view_history(self):

     history = ctk.CTkToplevel(self)

     history.title("Attendance History")
     history.geometry("800x500")
     history.grab_set()

     tree = ttk.Treeview(
        history,
        columns=(
            "attendance_id",
            "student",
            "date",
            "status",
        ),
        show="headings",
    )

     tree.heading("attendance_id", text="ID")
     tree.heading("student", text="Student")
     tree.heading("date", text="Date")
     tree.heading("status", text="Status")

     tree.column("attendance_id", width=60)
     tree.column("student", width=250)
     tree.column("date", width=120)
     tree.column("status", width=120)

     tree.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15,
    )

     self.load_history(tree)

     bottom = ctk.CTkFrame(
        history,
        fg_color="transparent",
    )

     bottom.pack(fill="x", pady=10)

     ctk.CTkButton(
        bottom,
        text="Refresh",
        command=lambda: self.load_history(tree),
    ).pack(side="left", padx=10)

     ctk.CTkButton(
        bottom,
        text="Toggle Status",
        command=lambda: self.toggle_status(tree),
    ).pack(side="left", padx=10)

     ctk.CTkButton(
        bottom,
        text="Delete",
        fg_color=COLORS["error"],
        command=lambda: self.delete_record(tree),
    ).pack(side="left", padx=10)        
     
    def load_history(self, tree):

     tree.delete(*tree.get_children())

     attendance_date = self.date_entry.get()

     try:

        rows = self.attendance_backend.get_all_history_with_names()

     except Exception as e:

        show_error(
            self,
            "Error",
            str(e)
        )
        return

     for row in rows:

        tree.insert(
            "",
            "end",
            iid=str(row[0]),
            values=row,
        ) 

    def toggle_status(self, tree):

     selection = tree.selection()

     if not selection:

        show_error(
            self,
            "Error",
            "Select a record first."
        )

        return

     attendance_id = int(selection[0])

     values = tree.item(selection[0])["values"]

     current_status = values[3]

     new_status = (
        "ABSENT"
        if current_status == "PRESENT"
        else "PRESENT"
    )

     try:

        self.attendance_backend.toggle_status(
            attendance_id,
            new_status,
        )

        self.load_history(tree)

        show_success(
            self,
            "Attendance updated."
        )

     except Exception as e:

        show_error(
            self,
            "Error",
            str(e),
        )    

    def delete_record(self, tree):

     selection = tree.selection()

     if not selection:

        show_error(
            self,
            "Error",
            "Select a record first."
        )

        return

     attendance_id = int(selection[0])

     try:

        self.attendance_backend.delete_by_id(
            attendance_id
        )

        self.load_history(tree)

        show_success(
            self,
            "Record deleted."
        )

     except Exception as e:
 
        show_error(
            self,
            "Error",
            str(e),
        )    