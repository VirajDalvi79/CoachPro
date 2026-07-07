import datetime
import customtkinter as ctk

from ui.theme import COLORS, FONTS
from ui.components.dialogs import show_success
from marks import Marks
from batch import Batch


class ExamFormDialog(ctk.CTkToplevel):

    def __init__(self, master, on_saved, exam_id=None):
        super().__init__(master)

        self.on_saved = on_saved
        self.exam_id = exam_id

        self.marks_backend = Marks()
        self.batch_backend = Batch()

        self.title("Edit Exam" if exam_id else "Create Exam")
        self.geometry("420x520")
        self.minsize(420, 520)
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg_surface"])

        self.transient(master)
        self.grab_set()

        self.batches = self.batch_backend.display_all_batches()
        self.batch_lookup = {b[1]: b[0] for b in self.batches}

        self._build_ui()

        if self.exam_id:
            self._load_existing()

    def _build_ui(self):

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(
            frame,
            text="Edit Exam" if self.exam_id else "Create Exam",
            font=FONTS["h2"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 16))

        self.exam_name_entry = self._entry(frame, "Exam Name *")

        self.exam_date_entry = self._entry(
            frame,
            "Exam Date (YYYY-MM-DD) *",
            datetime.date.today().isoformat()
        )

        self.total_marks_entry = self._entry(frame, "Total Marks *")

        ctk.CTkLabel(
            frame,
            text="Batch",
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(10, 4))

        batch_names = [b[1] for b in self.batches]

        self.batch_combo = ctk.CTkComboBox(
            frame,
            values=batch_names or ["No batches"],
            width=360,
            height=36,
            state="readonly" if batch_names else "disabled",
        )
        self.batch_combo.pack(fill="x")

        if batch_names:
            self.batch_combo.set(batch_names[0])

        self.error_label = ctk.CTkLabel(
            frame,
            text="",
            font=FONTS["small"],
            text_color=COLORS["error"],
            wraplength=360,
        )
        self.error_label.pack(anchor="w", pady=(8, 0))

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(pady=(18, 10))

        ctk.CTkButton(
            btn_row,
            text="Cancel",
            width=130,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["border"],
            text_color=COLORS["text_secondary"],
            command=self.destroy,
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btn_row,
            text="Save",
            width=130,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self._save,
        ).pack(side="left", padx=8)

    def _entry(self, parent, label, default=""):

        ctk.CTkLabel(
            parent,
            text=label,
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(10, 4))

        entry = ctk.CTkEntry(parent, width=360, height=36)
        entry.pack(fill="x")

        if default:
            entry.insert(0, default)

        return entry

    def _load_existing(self):

        row = self.marks_backend.get_exam_details(self.exam_id)

        if not row:
            self.destroy()
            return

        exam_id, exam_name, exam_date, total_marks, batch_id = row

        self.exam_name_entry.insert(0, exam_name)
        self.exam_date_entry.delete(0, "end")
        self.exam_date_entry.insert(0, str(exam_date))
        self.total_marks_entry.insert(0, str(total_marks))

        for b in self.batches:
            if b[0] == batch_id:
                self.batch_combo.set(b[1])
                break

    def _save(self):

        exam_name = self.exam_name_entry.get().strip()
        exam_date_text = self.exam_date_entry.get().strip()
        total_marks_text = self.total_marks_entry.get().strip()
        batch_name = self.batch_combo.get()
        batch_id = self.batch_lookup.get(batch_name)

        if not exam_name:
            self.error_label.configure(text="Exam name is required.")
            return

        try:
            exam_date = datetime.date.fromisoformat(exam_date_text)
        except ValueError:
            self.error_label.configure(text="Date must be YYYY-MM-DD.")
            return

        try:
            total_marks = float(total_marks_text)
        except ValueError:
            self.error_label.configure(text="Total marks must be a number.")
            return

        if total_marks <= 0:
            self.error_label.configure(text="Total marks must be greater than zero.")
            return

        if batch_id is None:
            self.error_label.configure(text="Please select a valid batch.")
            return

        try:
            if self.exam_id:
                self.marks_backend.update_exam(
                    self.exam_id,
                    exam_name,
                    exam_date,
                    total_marks,
                    batch_id,
                )
            else:
                self.marks_backend.create_exam(
                    exam_name,
                    exam_date,
                    total_marks,
                    batch_id,
                )

        except Exception as e:
            self.error_label.configure(text=f"Could not save exam: {e}")
            return

        self.destroy()
        show_success(self.master, "Exam saved successfully.")
        self.on_saved()