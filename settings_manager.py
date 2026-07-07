import json
import os


class SettingsManager:

    def __init__(self, file_name="settings.json"):
        self.file_name = file_name

        self.default_settings = {
            "institute_name": "CoachPro Academy",
            "address": "",
            "phone": "",
            "email": "",
            "logo_path": "",
            
        }

    def load_settings(self):

        if not os.path.exists(self.file_name):
            self.save_settings(self.default_settings)
            return self.default_settings

        with open(self.file_name, "r") as file:
            return json.load(file)

    def save_settings(self, settings):

        with open(self.file_name, "w") as file:
            json.dump(settings, file, indent=4)