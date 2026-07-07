from tkinter import ttk
import customtkinter as ctk

from ui.theme import COLORS, FONTS
from ui.components.dialogs import ConfirmDialog, show_success, show_error
from ui.components.subject_form_dialog import SubjectFormDialog
from marks import Marks
from batch import Batch


COLUMNS = ("subject_id", "subject_name", "batch")


class SubjectsPage(ctk.CTkFrame):

    def __init__(self, master, admin_info=None):
        super().__init__(master, fg_color="transparent")

        self.marks_backend = Marks()
        self.batch_backend = Batch()

        self._build_ui()
        self._refresh()

    def _build_ui(self):

        self._style_treeview()

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            header,
            text="Subjects",
            font=FONTS["h1"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="+ Add Subject",
            width=150,
            height=38,
            corner_radius=10,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self._open_add_dialog,
        ).pack(side="right")

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
            placeholder_text="Search subject name...",
            width=320,
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
            style="Subjects.Treeview",
        )

        self.tree.heading("subject_id", text="Subject ID")
        self.tree.heading("subject_name", text="Subject Name")
        self.tree.heading("batch", text="Batch")

        self.tree.column("subject_id", width=120, anchor="center")
        self.tree.column("subject_name", width=280, anchor="w")
        self.tree.column("batch", width=220, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=1, pady=1)
        self.tree.bind("<Double-1>", lambda e: self._open_edit_dialog())

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", pady=(12, 0))

        ctk.CTkButton(
            actions,
            text="Edit",
            width=100,
            height=36,
            corner_radius=10,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["border"],
            command=self._open_edit_dialog,
        ).pack(side="left")

        ctk.CTkButton(
            actions,
            text="Delete",
            width=110,
            height=36,
            corner_radius=10,
            fg_color="transparent",
            hover_color=COLORS["error"],
            text_color=COLORS["text_secondary"],
            command=self._confirm_delete,
        ).pack(side="left", padx=8)

    def _style_treeview(self):

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Subjects.Treeview",
            background=COLORS["bg_surface"],
            fieldbackground=COLORS["bg_surface"],
            foreground=COLORS["text_primary"],
            rowheight=38,
            borderwidth=0,
            font=FONTS["body"],
        )

        style.configure(
            "Subjects.Treeview.Heading",
            background=COLORS["bg_surface_alt"],
            foreground=COLORS["text_secondary"],
            borderwidth=0,
            font=FONTS["small"],
        )

        style.map(
            "Subjects.Treeview",
            background=[("selected", COLORS["accent_soft"])],
            foreground=[("selected", COLORS["text_primary"])],
        )

    def _batch_lookup(self):

        return {
            batch[0]: batch[1]
            for batch in self.batch_backend.display_all_batches()
        }

    def _format_subject_id(self, subject_id):

        return f"SUB-{int(subject_id):04d}"

    def _populate(self, rows):

        self.tree.delete(*self.tree.get_children())

        batch_names = self._batch_lookup()

        for subject_id, subject_name, batch_id in rows:

            self.tree.insert(
                "",
                "end",
                iid=str(subject_id),
                values=(
                    self._format_subject_id(subject_id),
                    subject_name.title(),
                    batch_names.get(batch_id, "—"),
                ),
            )

    def _refresh(self):

        self.search_entry.delete(0, "end")
        rows = self.marks_backend.get_all_subjects()
        self._populate(rows)

    def _search(self):

        keyword = self.search_entry.get().strip()

        if not keyword:
            self._refresh()
            return

        rows = self.marks_backend.search_subjects(keyword)
        self._populate(rows)

    def _selected_subject_id(self):

        selected = self.tree.selection()

        if not selected:
            return None

        return int(selected[0])

    def _open_add_dialog(self):

        SubjectFormDialog(
            self,
            on_saved=self._refresh,
        )

    def _open_edit_dialog(self):

        subject_id = self._selected_subject_id()

        if subject_id is None:
            show_error(self, "Select a subject first.")
            return

        SubjectFormDialog(
            self,
            on_saved=self._refresh,
            subject_id=subject_id,
        )

    def _confirm_delete(self):

        subject_id = self._selected_subject_id()

        if subject_id is None:
            show_error(self, "Select a subject first.")
            return

        ConfirmDialog(
            self,
            title="Delete Subject",
            message="This will delete the selected subject. Continue?",
            on_confirm=lambda: self._delete_subject(subject_id),
            confirm_text="Delete",
            danger=True,
        )

    def _delete_subject(self, subject_id):

        try:
            self.marks_backend.delete_subject(subject_id)
            show_success(self, "Subject deleted.")
            self._refresh()

        except Exception as e:
            show_error(self, "Error", str(e))