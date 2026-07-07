import datetime
import customtkinter as ctk
from tkinter import ttk

from ui.theme import COLORS, FONTS
from ui.components.dialogs import show_error, show_success

from student import Students
from payments import Payments
import os
from receipt_generator import generate_payment_receipt

class FeesPage(ctk.CTkFrame):

    def __init__(self, master, admin_info=None):

        super().__init__(master, fg_color="transparent")

        self.students_backend = Students()
        self.payments_backend = Payments()

        self.students_map = {}

        self._build_ui()
        self.after(100, self._load_students)
        

    # ---------------- UI ----------------

    def _build_ui(self):

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            header,
            text="Fees Management",
            font=FONTS["h1"],
            text_color=COLORS["text_primary"]
        ).pack(side="left")

        # ---------------- Student Select ----------------

        form = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"])
        form.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            form,
            text="Student",
            font=FONTS["body"]
        ).grid(row=0, column=0, padx=10, pady=10)
        
        self.student_search_entry = ctk.CTkEntry(
    form,
    width=240,
    placeholder_text="Search student..."
)

        self.student_search_entry.grid(
    row=0,
    column=2,
    padx=10,
    pady=10,
)

        self.student_search_entry.bind(
    "<KeyRelease>",
    lambda e: self.filter_students()
)
        self.student_combo = ctk.CTkComboBox(
    form,
    width=320,
    values=[],
    command=self.load_fee_details,
    dropdown_hover_color=COLORS["accent"],
)
        self.student_combo.grid(row=0, column=1, padx=10)

        # ---------------- Fee Info ----------------

        self.total_fee_label = ctk.CTkLabel(form, text="Total Fee: -")
        self.total_fee_label.grid(row=1, column=0, padx=10)

        self.paid_label = ctk.CTkLabel(form, text="Paid: -")
        self.paid_label.grid(row=1, column=1, padx=10)

        self.remaining_label = ctk.CTkLabel(form, text="Remaining: -")
        self.remaining_label.grid(row=1, column=2, padx=10)

        # ---------------- Payment Form ----------------

        pay_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"])
        pay_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(pay_frame, text="Amount", font=FONTS["body"]).grid(row=0, column=0)
        self.amount_entry = ctk.CTkEntry(pay_frame, width=200)
        self.amount_entry.grid(row=0, column=1, padx=10)

        ctk.CTkLabel(pay_frame, text="Date", font=FONTS["body"]).grid(row=0, column=2)
        self.date_entry = ctk.CTkEntry(pay_frame, width=150)
        self.date_entry.insert(0, str(datetime.date.today()))
        self.date_entry.grid(row=0, column=3, padx=10)

        ctk.CTkLabel(pay_frame, text="Remarks", font=FONTS["body"]).grid(row=1, column=0)
        self.remarks_entry = ctk.CTkEntry(pay_frame, width=300)
        self.remarks_entry.grid(row=1, column=1, columnspan=2, padx=10)

        ctk.CTkButton(
            pay_frame,
            text="Record Payment",
            fg_color=COLORS["accent"],
            command=self.record_payment
        ).grid(row=1, column=3, padx=10)

     # ---------------- History ----------------

        history_frame = ctk.CTkFrame(
              self,
        fg_color=COLORS["bg_surface"]
)
        history_frame.pack(
         fill="both",
         expand=True,
         padx=10,
         pady=10,
)

        self.tree = ttk.Treeview(
        history_frame,
        columns=("id", "amount", "date", "remarks"),
        show="headings"
)

        self.tree.heading("id", text="Payment ID")
        self.tree.heading("amount", text="Amount Paid")
        self.tree.heading("date", text="Payment Date")
        self.tree.heading("remarks", text="Remarks")

        self.tree.pack(
            fill="both",
            expand=True,
        )

        # ---------------- Buttons ----------------

        button_frame = ctk.CTkFrame(
            history_frame,
            fg_color="transparent"
        )
        button_frame.pack(
            fill="x",
            pady=10,
        )

        self.edit_btn = ctk.CTkButton(
            button_frame,
            text="Edit Payment",
            command=self.edit_payment,
        )
        self.edit_btn.pack(
            side="left",
            padx=5,
        )

        self.receipt_btn = ctk.CTkButton(
    button_frame,
    text="Generate Receipt",
    command=self.generate_receipt,
)

        self.receipt_btn.pack(
    side="left",
    padx=5,
)

        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete Payment",
            fg_color=COLORS["error"],
            command=self.delete_payment,
        )
        self.delete_btn.pack(
            side="left",
            padx=5,
        )

    # ---------------- Load Students ----------------

    def _load_students(self):

     try:
        students = self.students_backend.display_all_students()

     except Exception as e:
        print("DB ERROR:", e)
        return

     self.students_map = {}
     names = []

     for s in students:

        sid = s[0]
        name = s[1]

        self.students_map[name] = sid
        names.append(name)

     self.all_student_names = names

     if not hasattr(self, "student_combo"):
        print("Combo not ready yet")
        return

     self.student_combo.configure(values=names)

     if names:
        self.student_combo.set(names[0])
        self.load_fee_details(names[0])

    # ---------------- Load Fee Details ----------------

    def load_fee_details(self, student_name):

        student_id = self.students_map.get(student_name)

        self.selected_student_id = student_id

        total_fee = self.students_backend.get_student_details(student_id)[10]
        paid = self.payments_backend.total_paid(student_id)
        remaining = float(total_fee) - float(paid)

        self.total_fee_label.configure(text=f"Total Fee: ₹{total_fee}")
        self.paid_label.configure(text=f"Paid: ₹{paid}")
        self.remaining_label.configure(text=f"Remaining: ₹{remaining}")

        self.load_history(student_id)

    # ---------------- Load History ----------------

    def load_history(self, student_id):

        self.tree.delete(*self.tree.get_children())

        rows = self.payments_backend.payment_history(student_id)

        for r in rows:
            payment_id, amount, payment_date, remarks = r

            display_id = f"PAY-{int(payment_id):04d}"
            amount_display = f"₹{float(amount):,.2f}"

            self.tree.insert(
    "",
    "end",
    iid=str(payment_id),
    values=(
        display_id,
        amount_display,
        payment_date,
        remarks or "—",
    )
)

    # ---------------- Record Payment ----------------

    def record_payment(self):

        student_name = self.student_combo.get()
        student_id = self.students_map.get(student_name)

        amount = float(self.amount_entry.get())
        date = self.date_entry.get()
        remarks = self.remarks_entry.get()
        student = self.students_backend.get_student_details(student_id)

# Use the correct index where your total_fee is stored
        total_fee = float(student[10])

        paid = float(self.payments_backend.total_paid(student_id) or 0)

        remaining = total_fee - paid

# ---------------- Validation ----------------

        if amount <= 0:

         show_error(
        self,
        "Invalid Amount",
        "Payment amount must be greater than zero."
    )

         return

        if amount > remaining:

         show_error(
        self,
        "Payment Too Large",
        f"Remaining fee is only ₹{remaining:,.2f}"
    )

         return
        

        try:
            self.payments_backend.record_payment(
                student_id,
                amount,
                date,
                remarks
            )

            show_success(
    self,
    f"₹{amount:,.2f} recorded successfully."
)
            
            self.show_receipt(
    student_name=student_name,
    amount=amount,
    payment_date=date,
    remarks=remarks
)
            self.amount_entry.delete(0, "end")
            self.remarks_entry.delete(0, "end")

            self.load_fee_details(student_name)

        except Exception as e:
            show_error(self, str(e))

    def show_receipt(self, student_name, amount, payment_date, remarks):

     receipt = ctk.CTkToplevel(self)
     receipt.title("Payment Receipt")
     receipt.geometry("420x420")
     receipt.resizable(False, False)
     receipt.grab_set()

     frame = ctk.CTkFrame(
        receipt,
        fg_color=COLORS["bg_surface"],
        corner_radius=12
    )
     frame.pack(fill="both", expand=True, padx=20, pady=20)

     ctk.CTkLabel(
        frame,
        text="Payment Receipt",
        font=FONTS["h2"],
        text_color=COLORS["text_primary"]
     ).pack(pady=(10, 20))

     receipt_text = f"""
     Student: {student_name}

     Amount Paid: ₹{amount:,.2f}

    Payment Date: {payment_date}

    Remarks: {remarks if remarks else "—"}
"""

     ctk.CTkLabel(
        frame,
        text=receipt_text,
        font=FONTS["body"],
        text_color=COLORS["text_primary"],
        justify="left"
    ).pack(anchor="w", padx=30)

     ctk.CTkButton(
        frame,
        text="Close",
        command=receipt.destroy
    ).pack(pady=25)   
          

    def edit_payment(self):

     selected = self.tree.selection()

     if not selected:
        show_error(self, "Select Payment", "Please select a payment.")
        return

     payment = list(self.tree.item(selected[0])["values"])

     payment[0] = int(
        str(payment[0]).replace("PAY-", "")
    )

     EditPaymentDialog(
        self,
        payment,
        self.update_payment
    )

    def delete_payment(self):

     selected = self.tree.selection()
 
     if not selected:
        show_error(self, "Select Payment", "Please select a payment.")
        return

     payment = self.tree.item(selected[0])["values"]
     payment_id = payment[0]

     confirm = ctk.CTkInputDialog(
        text="Type YES to confirm deletion",
        title="Confirm Delete"
    )

     result = confirm.get_input()

     if result != "YES":
        return

     try:
        self.payments_backend.delete_payment(payment_id)

        self.load_history(self.selected_student_id)

        show_success(self, "Payment deleted successfully.")

     except Exception as e:
        show_error(self, "Error", str(e))



    def update_payment(self, payment_id, amount, date, remarks):

     try:
        self.payments_backend.update_payment(
            payment_id,
            float(amount.replace(",", "")),
            date,
            remarks
        )

        self.load_history(self.selected_student_id)

        show_success(self, "Payment updated successfully.")

     except Exception as e:
        show_error(self, "Error", str(e))


    def generate_receipt(self):

     selected = self.tree.selection()

     if not selected:
        show_error(
            self,
            "Select Payment",
            "Please select a payment first."
        )
        return

     payment = self.tree.item(selected[0])["values"]

     payment_id = int(str(payment[0]).replace("PAY-", ""))
     amount = str(payment[1]).replace("₹", "").replace(",", "")
     payment_date = payment[2]
     remarks = payment[3] if len(payment) > 3 else ""

     student_name = self.student_combo.get()

     student_id = self.students_map.get(student_name)
     student = self.students_backend.get_student_details(student_id)

     total_fee = float(student[10])
     paid = float(self.payments_backend.total_paid(student_id) or 0)
     remaining = total_fee - paid

     os.makedirs("receipts", exist_ok=True)

     file_path = os.path.join(
        "receipts",
        f"receipt_PAY-{payment_id:04d}.pdf"
    )

     try:
        generate_payment_receipt(
            file_path=file_path,
            payment_id=payment_id,
            student_name=student_name,
            amount=amount,
            payment_date=payment_date,
            remarks=remarks,
            remaining=remaining,
        )

        show_success(
            self,
            f"Receipt generated:\n{file_path}"
        )

     except Exception as e:
        show_error(
            self,
            "Receipt Error",
            str(e)
        )

    def filter_students(self):

     keyword = self.student_search_entry.get().strip().lower()

     filtered = []

     for name in self.all_student_names:

         if keyword in name.lower():
            filtered.append(name)

     self.student_combo.configure(values=filtered)

     if filtered:
        self.student_combo.set(filtered[0])
        self.load_fee_details(filtered[0])


class EditPaymentDialog(ctk.CTkToplevel):

    def __init__(self, master, payment_data, on_saved):
        super().__init__(master)

        self.payment_data = payment_data
        self.on_saved = on_saved

        self.title("Edit Payment")
        self.geometry("350x300")
        self.resizable(False, False)
        self.grab_set()

        self.build_ui()    


    def build_ui(self):

        payment_id, amount, date, remarks = self.payment_data

        self.amount_entry = ctk.CTkEntry(self)
        self.amount_entry.insert(0, amount)
        self.amount_entry.pack(pady=10)

        self.date_entry = ctk.CTkEntry(self)
        self.date_entry.insert(0, date)
        self.date_entry.pack(pady=10)

        self.remarks_entry = ctk.CTkEntry(self)
        self.remarks_entry.insert(0, remarks)
        self.remarks_entry.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Save",
            command=self.save
        ).pack(pady=20)    

    def save(self):

        payment_id, _, _, _ = self.payment_data

        amount = self.amount_entry.get()
        date = self.date_entry.get()
        remarks = self.remarks_entry.get()

        self.on_saved(payment_id, amount, date, remarks)

        self.destroy()    