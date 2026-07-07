from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from settings_manager import SettingsManager


def generate_report_card(
    file_path,
    student_name,
    student_id,
    exam_name,
    subjects,
    total_obtained,
    total_marks,
    percentage,
    grade,
):
    settings = SettingsManager().load_settings()
    institute_name = settings.get("institute_name", "CoachPro Academy")

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 25 * mm

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, y, institute_name)

    y -= 12 * mm
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, y, "Student Report Card")

    y -= 15 * mm
    c.line(20 * mm, y, width - 20 * mm, y)

    y -= 14 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(25 * mm, y, "Student ID:")
    c.setFont("Helvetica", 11)
    c.drawString(65 * mm, y, f"STU-{int(student_id):04d}")

    y -= 9 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(25 * mm, y, "Student Name:")
    c.setFont("Helvetica", 11)
    c.drawString(65 * mm, y, student_name)

    y -= 9 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(25 * mm, y, "Exam:")
    c.setFont("Helvetica", 11)
    c.drawString(65 * mm, y, exam_name)

    y -= 15 * mm

    c.setFont("Helvetica-Bold", 11)
    c.drawString(25 * mm, y, "Subject")
    c.drawString(110 * mm, y, "Marks")

    y -= 5 * mm
    c.line(25 * mm, y, width - 25 * mm, y)

    y -= 9 * mm
    c.setFont("Helvetica", 11)

    for subject_name, marks in subjects:
        c.drawString(25 * mm, y, str(subject_name))
        c.drawString(110 * mm, y, str(marks))
        y -= 8 * mm

    y -= 5 * mm
    c.line(25 * mm, y, width - 25 * mm, y)

    y -= 12 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(25 * mm, y, "Total:")
    c.drawString(65 * mm, y, f"{total_obtained} / {total_marks}")

    y -= 9 * mm
    c.drawString(25 * mm, y, "Percentage:")
    c.drawString(65 * mm, y, f"{percentage:.2f}%")

    y -= 9 * mm
    c.drawString(25 * mm, y, "Grade:")
    c.drawString(65 * mm, y, grade)

    y -= 25 * mm
    c.line(130 * mm, y, width - 25 * mm, y)

    y -= 6 * mm
    c.setFont("Helvetica", 9)
    c.drawString(142 * mm, y, "Authorized Signature")

    c.save()