import customtkinter as ctk
from tkinter import ttk

from ui.theme import COLORS, FONTS
from ui.components.dialogs import show_error, show_success

from marks import Marks
from batch import Batch
import os
from result_generator import generate_report_card

class MarksPage(ctk.CTkFrame):

    def __init__(self, master, admin_info=None):
        super().__init__(master, fg_color="transparent")

        self.marks_backend = Marks()
        self.batch_backend = Batch()

        self.batch_map = {}
        self.exam_map = {}
        self.subject_map = {}

        self.current_students = []
        self.mark_entries = {}

        self._build_ui()
        
     
    # Delay loading until the UI is ready
        self.after(100, self.load_batches)
        self.after(150, self.load_exams)

    def _build_ui(self):
        print("MARKS UI BUILDING")
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            header,
            text="Marks Management",
            font=FONTS["h1"],
            text_color=COLORS["text_primary"]
        ).pack(side="left")

        controls = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_surface"],
            corner_radius=12
        )
        controls.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(controls, text="Batch", font=FONTS["body"]).grid(row=0, column=0, padx=10, pady=12)

        self.batch_combo = ctk.CTkComboBox(
            controls,
            width=180,
            values=[],
            command=lambda value: self.load_subjects()
        )
        self.batch_combo.grid(row=0, column=1, padx=10)

        ctk.CTkLabel(controls, text="Exam", font=FONTS["body"]).grid(row=0, column=2, padx=10)

        self.exam_combo = ctk.CTkComboBox(
            controls,
            width=220,
            values=[]
        )
        self.exam_combo.grid(row=0, column=3, padx=10)

        ctk.CTkLabel(controls, text="Subject", font=FONTS["body"]).grid(row=0, column=4, padx=10)

        self.subject_combo = ctk.CTkComboBox(
            controls,
            width=180,
            values=[]
        )
        self.subject_combo.grid(row=0, column=5, padx=10)

        ctk.CTkButton(
            controls,
            text="Load Students",
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self.load_students
        ).grid(row=0, column=6, padx=10)

        ctk.CTkButton(
            controls,
            text="+ Exam",
            width=90,
            command=self.open_exam_dialog
        ).grid(row=0, column=7, padx=10)

        ctk.CTkButton(
            controls,
            text="+ Subject",
            width=100,
            command=self.open_subject_dialog
        ).grid(row=0, column=8, padx=10)

        list_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_surface"],
            corner_radius=12
        )
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.count_label = ctk.CTkLabel(
            list_frame,
            text="Students Loaded: 0",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"]
        )
        self.count_label.pack(anchor="w", padx=15, pady=(12, 5))

        self.scroll = ctk.CTkScrollableFrame(
            list_frame,
            fg_color="transparent"
        )
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkButton(
            bottom,
            text="Save Marks",
            width=150,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self.save_marks
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            bottom,
            text="View Results",
            width=150,
            command=self.view_results
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
    bottom,
    text="Generate Report Card",
    width=180,
    command=self.generate_report_card_pdf
).pack(side="left", padx=5)
        

    def load_batches(self):

     self.batch_map = {}

     batches = self.batch_backend.display_all_batches()

     names = []

     for batch in batches:

        batch_id = batch[0]
        batch_name = batch[1]

        self.batch_map[batch_name] = batch_id
        names.append(batch_name)

     self.batch_combo.configure(values=names)

     if names:
        self.batch_combo.set(names[0])
        self.load_subjects()    

    def load_exams(self):

     self.exam_map = {}

     exams = self.marks_backend.get_all_exams()

     names = []

     for exam in exams:

        exam_id = exam[0]
        exam_name = exam[1]

        self.exam_map[exam_name] = exam_id
        names.append(exam_name)

     self.exam_combo.configure(values=names)

     if names:
        self.exam_combo.set(names[0])    

    def load_subjects(self):

     batch_name = self.batch_combo.get()

     batch_id = self.batch_map.get(batch_name)

     self.subject_map = {}

     subjects = self.marks_backend.get_subjects_by_batch(batch_id)

     names = []

     for subject in subjects:

        subject_id = subject[0]
        subject_name = subject[1]

        self.subject_map[subject_name] = subject_id
        names.append(subject_name)

     self.subject_combo.configure(values=names)

     if names:
        self.subject_combo.set(names[0])    

    def load_students(self):

     for widget in self.scroll.winfo_children():
        widget.destroy()

     self.current_students.clear()
     self.mark_entries.clear()

     batch_name = self.batch_combo.get()
     batch_id = self.batch_map.get(batch_name)

     students = self.marks_backend.get_students_by_batch(batch_id)

     self.current_students = students

     self.count_label.configure(
         text=f"Students Loaded: {len(students)}"
    )

     for student_id, full_name in students:

        row = ctk.CTkFrame(
            self.scroll,
            fg_color=COLORS["bg_surface"],
            corner_radius=8
        )

        row.pack(
            fill="x",
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            row,
            text=f"STU-{int(student_id):04d}   {full_name.title()}",
            width=250,
            anchor="w",
            font=FONTS["body"]
        ).pack(
            side="left",
            padx=15,
            pady=10
        )

        entry = ctk.CTkEntry(
            row,
            width=100,
            placeholder_text="Marks"
        )
        
        exam_id = self.exam_map.get(self.exam_combo.get())
        subject_id = self.subject_map.get(self.subject_combo.get())

        existing = self.marks_backend.get_existing_mark(
    student_id,
    exam_id,
    subject_id
)

        if existing:
          entry.insert(0, str(existing[0]))

        entry.pack(
            side="right",
            padx=20
        )

        self.mark_entries[student_id] = entry    

    def save_marks(self):

     batch_name = self.batch_combo.get()
     exam_name = self.exam_combo.get()
     subject_name = self.subject_combo.get()

     exam_id = self.exam_map.get(exam_name)
     subject_id = self.subject_map.get(subject_name)

     saved = 0

     try:

        for student_id, full_name in self.current_students:

            marks_text = self.mark_entries[student_id].get().strip()

            if marks_text == "":
                continue

            marks = float(marks_text)

            self.marks_backend.save_or_update_marks(
                student_id,
                exam_id,
                subject_id,
                marks,
            )

            saved += 1

        show_success(
            self,
            f"{saved} marks saved successfully."
        )

     except Exception as e:

        show_error(
            self,
            "Error",
            str(e),
        )

    def view_results(self):

     exam_name = self.exam_combo.get()
     exam_id = self.exam_map.get(exam_name)

     if exam_id is None:
        show_error(self, "Error", "Select an exam first.")
        return

     rows = self.marks_backend.get_exam_results_with_names(exam_id)
     result_win = ctk.CTkToplevel(self)
     result_win.title("Exam Results")
     result_win.geometry("800x500")
     result_win.grab_set()

     tree = ttk.Treeview(
    result_win,
    columns=("student", "subject", "marks"),
    show="headings"
)

     tree.heading("student", text="Student")
     tree.heading("subject", text="Subject")
     tree.heading("marks", text="Marks")

     tree.pack(fill="both", expand=True, padx=15, pady=15)

     for row in rows:
        tree.insert("", "end", values=row)
     
    def open_exam_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Create Exam")
        dialog.geometry("360x360")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Exam Name").pack(pady=(20, 5))
        name_entry = ctk.CTkEntry(dialog, width=250)
        name_entry.pack()

        ctk.CTkLabel(dialog, text="Exam Date (YYYY-MM-DD)").pack(pady=(15, 5))
        date_entry = ctk.CTkEntry(dialog, width=250)
        date_entry.insert(0, "2026-07-03")
        date_entry.pack()

        ctk.CTkLabel(dialog, text="Total Marks").pack(pady=(15, 5))
        total_entry = ctk.CTkEntry(dialog, width=250)
        total_entry.pack()

        def save():
            try:
                batch_id = self.batch_map.get(self.batch_combo.get())
                self.marks_backend.create_exam(
                    name_entry.get().strip(),
                    date_entry.get().strip(),
                    float(total_entry.get().strip()),
                    batch_id
                )
                dialog.destroy()
                self.load_exams()
                show_success(self, "Exam created.")
            except Exception as e:
                show_error(self, "Error", str(e))

        ctk.CTkButton(dialog, text="Save", command=save).pack(pady=25) 


    def open_subject_dialog(self):
            dialog = ctk.CTkToplevel(self)
            dialog.title("Add Subject")
            dialog.geometry("340x220")
            dialog.grab_set()

            ctk.CTkLabel(dialog, text="Subject Name").pack(pady=(25, 5))
            subject_entry = ctk.CTkEntry(dialog, width=250)
            subject_entry.pack()

            def save():
                try:
                    batch_id = self.batch_map.get(self.batch_combo.get())
                    self.marks_backend.create_subject(
                        subject_entry.get().strip(),
                        batch_id
                    )
                    dialog.destroy()
                    self.load_subjects()
                    show_success(self, "Subject added.")
                except Exception as e:
                    show_error(self, "Error", str(e))

            ctk.CTkButton(dialog, text="Save", command=save).pack(pady=25)


    def generate_report_card_pdf(self):
        exam_name = self.exam_combo.get()
        exam_id = self.exam_map.get(exam_name)

        if exam_id is None:
            show_error(self, "Error", "Select an exam first.")
            return

        dialog = ctk.CTkInputDialog(
            text="Enter Student ID number only\nExample: 1",
            title="Generate Report Card"
        )

        student_id_text = dialog.get_input()

        if not student_id_text:
            return

        try:
            student_id = int(student_id_text)
        except ValueError:
            show_error(self, "Error", "Enter a valid student ID.")
            return

        student = None
        for sid, full_name in self.current_students:
            if sid == student_id:
                student = (sid, full_name)
                break

        if student is None:
            show_error(
                self,
                "Error",
                "Student not found in the currently loaded batch."
            )
            return

        try:
            rows = self.marks_backend.get_student_marks(student_id)

            subjects = []
            total_obtained = 0

            for row in rows:
                sid, row_exam_id, subject_id, marks_obtained = row

                if row_exam_id != exam_id:
                    continue

                subject_name = self._get_subject_name(subject_id)

                subjects.append(
                    (
                        subject_name,
                        float(marks_obtained)
                    )
                )

                total_obtained += float(marks_obtained)

            if not subjects:
                show_error(
                    self,
                    "No Marks",
                    "No marks found for this student and exam."
                )
                return

            marks_per_subject = float(self._get_exam_total_marks(exam_id))

            total_marks = marks_per_subject * len(subjects)

            percentage = (total_obtained / total_marks) * 100
            grade = self.marks_backend.calculate_grade(percentage)

            os.makedirs("report_cards", exist_ok=True)

            file_path = os.path.join(
                "report_cards",
                f"report_card_STU-{student_id:04d}_{exam_name}.pdf"
            )

            generate_report_card(
                file_path=file_path,
                student_name=student[1],
                student_id=student_id,
                exam_name=exam_name,
                subjects=subjects,
                total_obtained=total_obtained,
                total_marks=total_marks,
                percentage=percentage,
                grade=grade,
            )

            show_success(
                self,
                f"Report card generated:\n{file_path}"
            )

        except Exception as e:
            show_error(
                self,
                "Error",
                str(e)
            )        

    def _get_subject_name(self, subject_id):

     subjects = self.marks_backend.get_all_subjects()

     for sid, subject_name, batch_id in subjects:
        if sid == subject_id:
            return subject_name

     return f"Subject {subject_id}"


    def _get_exam_total_marks(self, exam_id):

     exams = self.marks_backend.get_all_exams()
 
     for eid, exam_name, exam_date, total_marks, batch_id in exams:
        if eid == exam_id:
            return total_marks

     return 0        