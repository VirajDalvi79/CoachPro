import os
import qrcode

from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from settings_manager import SettingsManager


CARD_SIZE = (86 * mm, 54 * mm)  # standard ID card size


def generate_student_id_card(
    file_path,
    student_id,
    student_name,
    phone,
    parent_phone,
    batch_name,
):
    settings = SettingsManager().load_settings()

    institute_name = settings.get(
        "institute_name",
        "CoachPro Academy"
    )

    logo_path = settings.get("logo_path", "")

    qr_data = f"STU-{int(student_id):04d}"

    os.makedirs("temp", exist_ok=True)

    qr_path = os.path.join(
        "temp",
        f"qr_STU-{int(student_id):04d}.png"
    )

    qr = qrcode.make(qr_data)
    qr.save(qr_path)

    c = canvas.Canvas(
        file_path,
        pagesize=landscape(CARD_SIZE)
    )

    width, height = landscape(CARD_SIZE)

    # Background
    c.setFillColor(colors.HexColor("#111827"))
    c.roundRect(
        0,
        0,
        width,
        height,
        8,
        fill=1,
        stroke=0
    )

    # Accent strip
    c.setFillColor(colors.HexColor("#2563eb"))
    c.roundRect(
        0,
        height - 10 * mm,
        width,
        10 * mm,
        8,
        fill=1,
        stroke=0
    )

    # Institute name
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(
        width / 2,
        height - 7 * mm,
        institute_name
    )

    # Logo placeholder / logo
    if logo_path and os.path.exists(logo_path):
        c.drawImage(
            logo_path,
            6 * mm,
            height - 9 * mm,
            width=7 * mm,
            height=7 * mm,
            mask="auto"
        )

    # Title
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#93c5fd"))
    c.drawString(
        6 * mm,
        height - 17 * mm,
        "STUDENT ID CARD"
    )

    # Student ID
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.white)
    c.drawString(
        6 * mm,
        height - 25 * mm,
        f"STU-{int(student_id):04d}"
    )

    # Student Name
    c.setFont("Helvetica-Bold", 10)
    c.drawString(
        6 * mm,
        height - 32 * mm,
        student_name[:28]
    )

    # Batch / phone
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#d1d5db"))

    c.drawString(
        6 * mm,
        height - 38 * mm,
        f"Batch: {batch_name}"
    )

    c.drawString(
        6 * mm,
        height - 43 * mm,
        f"Phone: {phone or '-'}"
    )

    c.drawString(
        6 * mm,
        height - 48 * mm,
        f"Parent: {parent_phone or '-'}"
    )

    # QR Code
    c.drawImage(
        qr_path,
        width - 23 * mm,
        7 * mm,
        width=17 * mm,
        height=17 * mm,
        mask="auto"
    )

    c.setFont("Helvetica", 5)
    c.setFillColor(colors.HexColor("#9ca3af"))
    c.drawCentredString(
        width - 14.5 * mm,
        4 * mm,
        "Scan ID"
    )

    c.save()