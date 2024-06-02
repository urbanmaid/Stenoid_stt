import json
import os

class LocaleManager:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'locales', 'ko_kr.json')
        with open(file = file_path, mode = 'r', encoding = 'UTF8') as file:
            self.data = json.load(file)

#print(data["status_idle"])  # Output: Idle
#print(data["status_recording"])  # Output: Tap Stop to convert to text.