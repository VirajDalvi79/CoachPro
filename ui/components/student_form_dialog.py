"""
ui/components/student_form_dialog.py

Add/Edit Student dialog. Editing pre-fills every field from
Students.get_student_details() so the admin only changes what's
needed, per the UI Philosophy doc, rather than retyping everything.
Also doubles as the "View Details" screen (Students page requirement)
since it already shows every field.
"""

import datetime
import customtkinter as ctk

from ui.theme import COLORS, FONTS
from ui.components.dialogs import show_success, show_error
from student import Students
from batch import Batch


class StudentFormDialog(ctk.CTkToplevel):
    def __init__(self, master, on_saved, student_id=None):
        super().__init__(master)
        self.on_saved = on_saved
        self.student_id = student_id
        self.students_backend = Students()
        self.batch_backend = Batch()

        self.title("Edit Student" if student_id else "Add Student")
        self.geometry("480x660")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg_surface"])
        self.transient(master)
        self.grab_set()

        # (batch_id, batch_name, start_time, end_time, classroom)
        self.batches = self.batch_backend.display_all_batches()
        self.batch_lookup = {b[1]: b[0] for b in self.batches}

        self._build_ui()
        self._center(master)

        if student_id:
            self._load_existing()

    def _center(self, master):
        self.update_idletasks()
        w, h = 480, 660
        x = master.winfo_rootx() + (master.winfo_width() // 2) - (w // 2)
        y = master.winfo_rooty() + (master.winfo_height() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=(24, 8))

        ctk.CTkLabel(
            scroll, text="Edit Student" if self.student_id else "Add Student",
            font=FONTS["h2"], text_color=COLORS["text_primary"]
        ).pack(anchor="w", pady=(0, 16))

        self.full_name_entry = self._labeled_entry(scroll, "Full Name *")
        self.phone_entry = self._labeled_entry(scroll, "Phone")
        self.father_entry = self._labeled_entry(scroll, "Father's Name")
        self.mother_entry = self._labeled_entry(scroll, "Mother's Name")
        self.parent_phone_entry = self._labeled_entry(scroll, "Parent's Phone")
        self.total_fee_entry = self._labeled_entry(
    scroll,
    "Total Course Fee *"
)

        ctk.CTkLabel(
            scroll, text="Batch", font=FONTS["small"], text_color=COLORS["text_secondary"]
        ).pack(anchor="w", pady=(10, 4))

        batch_names = [b[1] for b in self.batches]
        self.batch_combo = ctk.CTkComboBox(
            scroll, values=batch_names or ["No batches yet — add one first"],
            width=400, height=36, corner_radius=8,
            state="readonly" if batch_names else "disabled"
        )
        self.batch_combo.pack(fill="x")
        if batch_names:
            self.batch_combo.set(batch_names[0])

        self.admission_date_entry = self._labeled_entry(
            scroll, "Admission Date (YYYY-MM-DD) *",
            default=datetime.date.today().isoformat()
        )
        self.remarks_entry = self._labeled_entry(scroll, "Remarks")

        self.error_label = ctk.CTkLabel(
            scroll, text="", font=FONTS["small"], text_color=COLORS["error"], wraplength=400
        )
        self.error_label.pack(anchor="w", pady=(8, 0))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=16)

        ctk.CTkButton(
            btn_row, text="Cancel", width=130, height=38, corner_radius=8,
            fg_color=COLORS["bg_surface_alt"], hover_color=COLORS["border"],
            text_color=COLORS["text_secondary"], command=self.destroy
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btn_row, text="Save", width=130, height=38, corner_radius=8,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=self._save
        ).pack(side="left", padx=8)

    def _labeled_entry(self, parent, label, default=""):
        ctk.CTkLabel(
            parent, text=label, font=FONTS["small"], text_color=COLORS["text_secondary"]
        ).pack(anchor="w", pady=(10, 4))
        entry = ctk.CTkEntry(parent, width=400, height=36, corner_radius=8)
        entry.pack(fill="x")
        if default:
            entry.insert(0, default)
        return entry

    def _load_existing(self):
        row = self.students_backend.get_student_details(self.student_id)
        if row is None:
            show_error(self.master, "Student not found.")
            self.destroy()
            return

        # students table column order (schema.sql):
        # student_id, full_name, phone, father_name, mother_name,
        # parent_phone, batch_id, admission_date, remarks, status
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
        ) = row

        self.full_name_entry.insert(0, full_name or "")
        self.phone_entry.insert(0, phone or "")
        self.father_entry.insert(0, father_name or "")
        self.mother_entry.insert(0, mother_name or "")
        self.parent_phone_entry.insert(0, parent_phone or "")

        self.admission_date_entry.delete(0, "end")
        self.admission_date_entry.insert(0, str(admission_date))

        self.remarks_entry.insert(0, remarks or "")
        self.total_fee_entry.insert(0, str(total_fee))

        for b in self.batches:
            if b[0] == batch_id:
                self.batch_combo.set(b[1])
                break

    def _save(self):
        full_name = self.full_name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        father_name = self.father_entry.get().strip()
        mother_name = self.mother_entry.get().strip()
        parent_phone = self.parent_phone_entry.get().strip()
        batch_name = self.batch_combo.get()
        batch_id = self.batch_lookup.get(batch_name)
        admission_date_text = self.admission_date_entry.get().strip()
        remarks = self.remarks_entry.get().strip()

        if not full_name:
            self.error_label.configure(text="Full name is required.")
            return

        if not parent_phone:
            self.error_label.configure(text="Parent phone is required.")
            return

        if phone and not phone.isdigit():
            self.error_label.configure(text="Phone number should contain digits only.")
            return

        if parent_phone and not parent_phone.isdigit():
            self.error_label.configure(text="Parent phone should contain digits only.")
            return

        if batch_id is None:
            self.error_label.configure(text="Please select a valid batch.")
            return

        try:
            admission_date = datetime.date.fromisoformat(admission_date_text)
        except ValueError:
            self.error_label.configure(text="Admission date must be YYYY-MM-DD.")
            return

        try:
            total_fee = float(self.total_fee_entry.get().strip().replace(",", ""))
        except ValueError:
            self.error_label.configure(text="Enter a valid total fee.")
            return

        if total_fee < 0:
            self.error_label.configure(text="Total fee cannot be negative.")
            return

        try:
            if self.student_id:
                self.students_backend.update_student(
                    full_name,
                    phone,
                    father_name,
                    mother_name,
                    parent_phone,
                    batch_id,
                    admission_date,
                    remarks,
                    total_fee,
                    self.student_id,
                )
            else:
                self.students_backend.create_student(
                    full_name,
                    phone,
                    father_name,
                    mother_name,
                    parent_phone,
                    batch_id,
                    admission_date,
                    remarks,
                    total_fee,
                )

        except Exception as e:
            self.error_label.configure(text=f"Could not save: {e}")
            return

        master = self.master
        on_saved = self.on_saved

        self.destroy()

        show_success(master, "Student saved successfully.")

        on_saved()