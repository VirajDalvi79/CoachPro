import json
import os
import sys
import mysql.connector
from tkinter import messagebox


def app_base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


CONFIG_FILE = os.path.join(app_base_dir(), "config.json")


def load_db_config():

    default_config = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "",
        "database": "coachpro_db",
    }

    if not os.path.exists(CONFIG_FILE):

        with open(CONFIG_FILE, "w") as file:
            json.dump(default_config, file, indent=4)

        messagebox.showerror(
            "Database Config Missing",
            f"config.json was created here:\n\n{CONFIG_FILE}\n\nPlease edit it and restart the app."
        )

        raise SystemExit

    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)

    # auto-upgrade old config files
    changed = False

    if "port" not in config:
        config["port"] = 3306
        changed = True

    if config.get("host") == "localhost":
        config["host"] = "127.0.0.1"
        changed = True

    if changed:
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)

    return config


try:
    config = load_db_config()

    connection = mysql.connector.connect(
    host=config["host"],
    port=int(config.get("port", 3306)),
    user=config["user"],
    password=config["password"],
    database=config["database"],
    connection_timeout=5,
    use_pure=True,
)

    cursor = connection.cursor()

    print("[Database] Connection successful.")

except Exception as e:
    messagebox.showerror(
        "Database Connection Error",
        f"Could not connect to database.\n\n{e}"
    )
    raise