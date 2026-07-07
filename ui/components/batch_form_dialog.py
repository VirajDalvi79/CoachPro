"""
ui/components/batch_form_dialog.py

Reusable dialog for both:

• Add Batch
• Edit Batch
"""

import datetime
import customtkinter as ctk

from batch import Batch
from ui.theme import COLORS, FONTS
from ui.components.dialogs import show_success


class BatchFormDialog(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        on_saved,
        batch_data=None
    ):
        super().__init__(master)

        self.batch_backend = Batch()
        self.on_saved = on_saved
        self.batch_data = batch_data

        self.title(
            "Edit Batch"
            if batch_data
            else "Add Batch"
        )

        self.geometry("430x600")
        self.resizable(False, False)

        self.configure(
            fg_color=COLORS["bg_surface"]
        )

        self.transient(master)
        self.grab_set()
        self.minsize(430, 600)

        self._build_ui()

        if self.batch_data:
            self._load_batch()

        self._center(master)

    def _center(self, master):

        self.update_idletasks()

        width = 430
        height = 470

        x = master.winfo_rootx() + (
            master.winfo_width() // 2
        ) - width // 2

        y = master.winfo_rooty() + (
            master.winfo_height() // 2
        ) - height // 2

        self.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    def _build_ui(self):

        frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        ctk.CTkLabel(
            frame,
            text="Edit Batch"
            if self.batch_data
            else "Add Batch",
            font=FONTS["h2"],
            text_color=COLORS["text_primary"]
        ).pack(
            anchor="w",
            pady=(0,20)
        )

        self.name_entry = self._entry(
            frame,
            "Batch Name *"
        )

        self.start_entry = self._entry(
            frame,
            "Start Time (HH:MM)",
            "09:00"
        )

        self.end_entry = self._entry(
            frame,
            "End Time (HH:MM)",
            "10:00"
        )

        self.classroom_entry = self._entry(
            frame,
            "Classroom"
        )

        self.error_label = ctk.CTkLabel(
            frame,
            text="",
            font=FONTS["small"],
            text_color=COLORS["error"]
        )

        self.error_label.pack(
            anchor="w",
            pady=(10,0)
        )

        button_row = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        button_row.pack(pady=(20, 10), fill="x")

        ctk.CTkButton(
            button_row,
            text="Cancel",
            width=140,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["border"],
            text_color=COLORS["text_secondary"],
            command=self.destroy
        ).pack(
            side="left",
            padx=8
        )

        ctk.CTkButton(
            button_row,
            text="Save",
            width=140,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self._save
        ).pack(
            side="left",
            padx=8
        )

    def _entry(
        self,
        parent,
        label,
        default=""
    ):

        ctk.CTkLabel(
            parent,
            text=label,
            font=FONTS["small"],
            text_color=COLORS["text_secondary"]
        ).pack(
            anchor="w",
            pady=(10,4)
        )

        entry = ctk.CTkEntry(
            parent,
            width=360,
            height=38
        )

        entry.pack(
            fill="x"
        )

        if default:
            entry.insert(
                0,
                default
            )

        return entry

    def _load_batch(self):

        self.name_entry.delete(0, "end")
        self.name_entry.insert(
            0,
            self.batch_data[1]
        )

        self.start_entry.delete(0, "end")
        self.start_entry.insert(
            0,
            str(self.batch_data[2])[:5]
        )

        self.end_entry.delete(0, "end")
        self.end_entry.insert(
            0,
            str(self.batch_data[3])[:5]
        )

        self.classroom_entry.delete(0, "end")
        self.classroom_entry.insert(
            0,
            self.batch_data[4] or ""
        )
    def _save(self):

         name = self.name_entry.get().strip()
         start_text = self.start_entry.get().strip()
         end_text = self.end_entry.get().strip()
         classroom = self.classroom_entry.get().strip()

         if not name:
            self.error_label.configure(
                text="Batch name is required."
            )
            return

         try:

            start_time = datetime.datetime.strptime(
               start_text,
                "%H:%M"
            ).time()

            end_time = datetime.datetime.strptime(
                end_text,
                "%H:%M"
            ).time()

         except ValueError:

            self.error_label.configure(
                text="Time must be in HH:MM format."
            )
            return

         try:

            if self.batch_data:

                self.batch_backend.update_batch(
                    self.batch_data[0],
                    name,
                    start_time,
                    end_time,
                    classroom
                )

                message = "Batch updated successfully."

            else:

                self.batch_backend.create_batch(
                    name,
                    start_time,
                    end_time,
                    classroom
                )

                message = "Batch created successfully."

         except Exception as e:

            self.error_label.configure(
                text=str(e)
            )
            return

         self.destroy()

         show_success(
             self.master,
            message
        )

         self.on_saved()