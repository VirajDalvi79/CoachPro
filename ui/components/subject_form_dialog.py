import customtkinter as ctk

from ui.theme import COLORS, FONTS
from ui.components.dialogs import show_success
from marks import Marks
from batch import Batch


class SubjectFormDialog(ctk.CTkToplevel):

    def __init__(self, master, on_saved, subject_id=None):
        super().__init__(master)

        self.on_saved = on_saved
        self.subject_id = subject_id

        self.marks_backend = Marks()
        self.batch_backend = Batch()

        self.title("Edit Subject" if subject_id else "Add Subject")
        self.geometry("400x380")
        self.minsize(400, 380)
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg_surface"])
        self.grab_set()

        self.batches = self.batch_backend.display_all_batches()
        self.batch_lookup = {b[1]: b[0] for b in self.batches}

        self._build_ui()

        if subject_id:
            self._load_existing()

    def _build_ui(self):

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(
            frame,
            text="Edit Subject" if self.subject_id else "Add Subject",
            font=FONTS["h2"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 16))

        ctk.CTkLabel(
            frame,
            text="Subject Name *",
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(10, 4))

        self.subject_entry = ctk.CTkEntry(frame, width=340, height=36)
        self.subject_entry.pack(fill="x")

        ctk.CTkLabel(
            frame,
            text="Batch",
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(12, 4))

        batch_names = [b[1] for b in self.batches]

        self.batch_combo = ctk.CTkComboBox(
            frame,
            values=batch_names or ["No batches"],
            width=340,
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
        )
        self.error_label.pack(anchor="w", pady=(8, 0))

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(pady=(18, 10))

        ctk.CTkButton(
            row,
            text="Cancel",
            width=120,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["border"],
            command=self.destroy,
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            row,
            text="Save",
            width=120,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self._save,
        ).pack(side="left", padx=8)

    def _load_existing(self):

        row = self.marks_backend.get_subject_details(self.subject_id)

        if not row:
            self.destroy()
            return

        subject_id, subject_name, batch_id = row

        self.subject_entry.insert(0, subject_name)

        for b in self.batches:
            if b[0] == batch_id:
                self.batch_combo.set(b[1])
                break

    def _save(self):

        subject_name = self.subject_entry.get().strip()
        batch_name = self.batch_combo.get()
        batch_id = self.batch_lookup.get(batch_name)

        if not subject_name:
            self.error_label.configure(text="Subject name is required.")
            return

        if batch_id is None:
            self.error_label.configure(text="Please select a valid batch.")
            return

        try:
            if self.subject_id:
                self.marks_backend.update_subject(
                    self.subject_id,
                    subject_name,
                    batch_id,
                )
            else:
                self.marks_backend.create_subject(
                    subject_name,
                    batch_id,
                )

        except Exception as e:
            self.error_label.configure(text=f"Could not save subject: {e}")
            return

        self.destroy()
        show_success(self.master, "Subject saved successfully.")
        self.on_saved()