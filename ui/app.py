"""
ui/app.py

Main application window.
Acts as the page router for the Coaching Management System.
"""

import customtkinter as ctk
import os
import sys

from ui.pages.marks import MarksPage
from ui.theme import COLORS
from ui.components.sidebar import Sidebar
from ui.pages.dashboard import DashboardPage
from ui.pages.students import StudentsPage
from ui.pages.batches import BatchesPage
from ui.pages.attendance import AttendancePage
from ui.pages.fees import FeesPage
from ui.pages.reports import ReportsPage
from ui.pages.settings import SettingsPage
from ui.pages.student_V2 import StudentsPageV2
from ui.pages.batches_V2 import BatchesPageV2
from ui.pages.exams import ExamsPage
from ui.pages.subjects import SubjectsPage

class MainWindow(ctk.CTk):

    def __init__(self, admin_info):
        super().__init__()
        self.after(200, self.set_app_icon)
        

        if getattr(sys, "frozen", False):
         icon_path = os.path.join(sys._MEIPASS, "coachpro.ico")
        else:
         icon_path = "coachpro.ico"

        try:
         self.iconbitmap(icon_path)
        except Exception as e:
         print("Icon error:", e)
        
        try:
         self.iconbitmap("coachpro.ico")
        except Exception:
         pass

        self.admin_info = admin_info

        self.title("Coaching Management System")
        self.geometry("1200x720")
        self.minsize(1000, 640)

        self.configure(
            fg_color=COLORS["bg_app"]
        )

        # -----------------------------------------
        # Page Registry
        # -----------------------------------------

        self.pages = {}
        self._current_page = None

        self.page_classes = {
    "dashboard": DashboardPage,
    "students": StudentsPageV2,
    "batches": BatchesPageV2,
    "attendance": AttendancePage,
    "fees": FeesPage,
    "reports": ReportsPage,
    "marks": MarksPage,
    "settings": SettingsPage,
    "exams": ExamsPage,
    "subjects": SubjectsPage,
}

        # -----------------------------------------
        # Sidebar
        # -----------------------------------------

        self.sidebar = Sidebar(
            self,
            on_navigate=self._navigate,
            on_logout=self._logout,
            admin_name=admin_info.get(
                "full_name",
                "Admin",
            ),
        )

        self.sidebar.pack(
            side="left",
            fill="y",
        )

        # -----------------------------------------
        # Main Content Area
        # -----------------------------------------

        self.content = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_app"],
            corner_radius=0,
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True,
        )

        # -----------------------------------------
        # Open Dashboard
        # -----------------------------------------

        self.sidebar._select("dashboard")

    # =====================================================
    # Navigation
    # =====================================================

    def _navigate(self, page_key):

        if self._current_page is not None:
            self._current_page.pack_forget()

        page_class = self.page_classes.get(page_key)

        if page_class is None:
            return

        if page_key not in self.pages:

            self.pages[page_key] = page_class(
                self.content,
                self.admin_info,
            )

        self._current_page = self.pages[page_key]

        self._current_page.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30,
        )
        if hasattr(self._current_page, "load_batches"):
         self._current_page.load_batches()


         
    # =====================================================
    # Logout
    # =====================================================

    def _logout(self):

        self.destroy()

        from ui.login import LoginWindow
        from main import launch_main_window

        login = LoginWindow(
            on_success=launch_main_window
        )

        login.mainloop()

    def set_app_icon(self):
     try:
        if getattr(sys, "frozen", False):
            icon_path = os.path.join(sys._MEIPASS, "coachpro.ico")
        else:
            icon_path = os.path.join(os.getcwd(), "coachpro.ico")

        self.iconbitmap(icon_path)

     except Exception as e:
        print("Icon error:", e)    