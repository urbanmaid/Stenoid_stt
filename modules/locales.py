import json
import os
settings_file = "settings.json"

class LocaleManager:
    def __init__(self):
        # settings.json 파일을 읽기 모드로 엽니다.
        with open(settings_file, 'r') as file:
            try:
                self.settingsList = json.load(file)
            except json.JSONDecodeError:
                print("Error of Opening Setting files.")

        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'locales', self.settingsList["language"])
        with open(file = file_path, mode = 'r', encoding = 'UTF8') as file:
            self.data = json.load(file)

        #print(os.listdir(os.path.join(current_dir, 'locales')))