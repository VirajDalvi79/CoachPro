# 🎓 CoachPro Management System

<p align="center">
  <img src="screenshots/logo.png" width="180" alt="CoachPro Logo">
</p>

<p align="center">
  <strong>A modern Coaching Institute Management System built with Python, CustomTkinter, and MySQL.</strong>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

## 📖 Overview

CoachPro is a complete desktop application designed for coaching institutes to efficiently manage students, attendance, fees, examinations, report cards, and administrative tasks.

The project was built using **Python**, **CustomTkinter**, and **MySQL**, providing a modern desktop interface with reliable database management and professional reporting features.

---

# ✨ Features

## 👨‍💼 Administration

- Secure Admin Login
- First-Time Admin Setup
- Institute Settings
- Database Backup

---

## 👨‍🎓 Student Management

- Add Students
- Edit Student Details
- Search Students
- Student Profiles
- Admission Information

---

## 📚 Batch Management

- Create Batches
- Assign Students
- Manage Batch Information

---

## 📅 Attendance Management

- Daily Attendance
- Present / Absent Tracking
- Attendance Reports

---

## 📝 Examination Management

- Create Exams
- Manage Subjects
- Enter Student Marks
- Automatic Percentage Calculation
- Grade Calculation

---

## 💰 Fee Management

- Student Fee Records
- Record Payments
- Edit Payments
- Delete Payments
- Remaining Balance Calculation

---

## 📄 Reports

- Professional Report Cards
- Fee Receipts (PDF)
- Student ID Cards
- QR Code Generation

---

## 🎨 Modern User Interface

- Clean Dashboard
- Responsive Navigation
- Professional Layout
- Modern CustomTkinter Design

---

# 🖥️ Screenshots

| Dashboard | Students |
|------------|----------|
| ![](screenshots/dashboard.png) | ![](screenshots/students.png) |

| Attendance | Fees |
|------------|------|
| ![](screenshots/attendance.png) | ![](screenshots/fees.png) |

| Report Card | Settings |
|-------------|----------|
| ![](screenshots/report_card.png) | ![](screenshots/settings.png) |

---

# 🛠️ Tech Stack

- Python 3.13
- CustomTkinter
- MySQL
- mysql-connector-python
- ReportLab
- qrcode
- Pillow
- PyInstaller
- Inno Setup

---

# 📂 Project Structure

```
CoachPro/
│
├── ui/
├── assets/
├── reports/
├── receipts/
├── id_cards/
├── temp/
│
├── database.py
├── admin.py
├── main.py
├── schema.sql
├── config.json
├── settings.json
│
├── coachpro.ico
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CoachPro.git
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Install MySQL Community Server

Create a database:

```sql
CREATE DATABASE coachpro_db;
```

Import the schema:

```sql
SOURCE schema.sql;
```

---

## 4. Configure Database

Edit **config.json**

```json
{
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "YOUR_PASSWORD",
    "database": "coachpro_db"
}
```

---

## 5. Run the application

```bash
python main.py
```

---

# 📦 Build Executable

```bash
pyinstaller --clean --noconfirm --onedir --windowed --icon coachpro.ico --add-data "coachpro.ico;." --name CoachPro main.py
```

---

# 🚀 Windows Installer

The project includes a professional Windows installer built using **Inno Setup**.

---

# 📈 Future Improvements

- Cloud Synchronization
- Multi-User Support
- Role-Based Access
- Online License Activation
- Automatic Updates
- WhatsApp Notifications
- SMS Notifications
- Student Portal
- Parent Portal
- Analytics Dashboard

---

# 🤝 Contributing

Contributions, feature requests, and bug reports are welcome.

Feel free to fork the project and submit a pull request.

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Developer

**Viraj Dalvi**

GitHub:
https://github.com/VirajDalvi79

---

# ⭐ Support

If you like this project, please consider giving it a ⭐ on GitHub.

It helps others discover the project and supports future development.
