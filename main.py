"""
main.py
"""

try:
    print("Importing theme...")
    from ui.theme import apply_theme

    print("Importing login...")
    from ui.login import LoginWindow

    print("Importing app...")
    from ui.app import MainWindow

    print("Importing setup admin...")
    from ui.setup_admin import SetupAdminWindow

    print("Importing admin...")
    from admin import Admin

    print("ALL IMPORTS OK")

except BaseException as e:
    print("IMPORT ERROR:", repr(e))
    input("Press Enter to exit...")
    raise


def launch_main_window(admin_info):
    app = MainWindow(admin_info)
    app.mainloop()


def launch_login():
    login = LoginWindow(on_success=launch_main_window)
    login.mainloop()


def main():
    apply_theme()

    admin_backend = Admin()

    if admin_backend.admin_exists():
        launch_login()
    else:
        setup = SetupAdminWindow(on_success=launch_login)
        setup.mainloop()


if __name__ == "__main__":
    main()