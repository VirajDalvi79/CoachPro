from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from settings_manager import SettingsManager


def generate_payment_receipt(
    file_path,
    payment_id,
    student_name,
    amount,
    payment_date,
    remarks,
    remaining,
):
    settings = SettingsManager().load_settings()
    institute_name = settings.get("institute_name", "CoachPro Academy")

    c = canvas.Canvas(file_path, pagesize=A5)
    width, height = A5

    y = height - 25 * mm

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, y, institute_name)

    y -= 10 * mm
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, y, "Payment Receipt")

    y -= 12 * mm
    c.line(20 * mm, y, width - 20 * mm, y)

    y -= 15 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(25 * mm, y, "Receipt ID:")
    c.setFont("Helvetica", 11)
    c.drawString(65 * mm, y, f"PAY-{int(payment_id):04d}")

    y -= 10 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(25 * mm, y, "Student:")
    c.setFont("Helvetica", 11)
    c.drawString(65 * mm, y, student_name)

    y -= 10 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(25 * mm, y, "Amount Paid:")
    c.setFont("Helvetica", 11)
    c.drawString(65 * mm, y, f"Rs. {float(amount):,.2f}")

    y -= 10 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(25 * mm, y, "Date:")
    c.setFont("Helvetica", 11)
    c.drawString(65 * mm, y, str(payment_date))

    y -= 10 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(25 * mm, y, "Remaining:")
    c.setFont("Helvetica", 11)
    c.drawString(65 * mm, y, f"Rs. {float(remaining):,.2f}")

    y -= 10 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(25 * mm, y, "Remarks:")
    c.setFont("Helvetica", 11)
    c.drawString(65 * mm, y, remarks if remarks else "-")

    y -= 18 * mm
    c.setStrokeColor(colors.grey)
    c.line(25 * mm, y, width - 25 * mm, y)

    y -= 8 * mm
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2, y, "This is a computer-generated receipt.")

    c.save()