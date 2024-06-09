import customtkinter
import json
import os
import tkinter
import webbrowser

from modules.ui_margins import UIMargins
from modules.locales import LocaleManager

#app = customtkinter.CTk()
current_dir = os.path.dirname(__file__)
languageList = os.listdir(os.path.join(current_dir, 'locales'))
default_settings = {
    "language": "en_us.json",
    "api_key": "0",
    "use_rich_punc": 1,
    "max_record_len": 30.0,
    "max_token": 200.0,
    "detection_languages": [
        "English",
        "Spanish"
    ]
}
settings_file = "settings.json"
locale = LocaleManager()
versioninfo = "24.06.09"

class Settings:
    def __init__(self, basis):
        self.settingsWindow = ""
        self.basis = basis
        self.uiMargins = UIMargins()

        # settings.json 파일이 없거나 비어 있으면 기본 설정 값으로 초기화
        if not os.path.exists(settings_file) or os.stat(settings_file).st_size == 0:
            with open(settings_file, 'w') as file:
                json.dump(default_settings, file, indent=4)

        # settings.json 파일을 읽기 모드로 엽니다.
        with open(settings_file, 'r') as file:
            try:
                self.settingsList = json.load(file)
            except json.JSONDecodeError:
                # JSONDecodeError가 발생하면 기본 설정 값으로 초기화
                self.settingsList = default_settings
                with open(settings_file, 'w') as file:
                    json.dump(default_settings, file, indent=4)

    def loadSettings(self):
        self.languageSelection.set(self.settingsList["language"])
        self.apiKey.delete("1.0", tkinter.END)
        self.apiKey.insert(tkinter.END, self.settingsList["api_key"])
        if (self.settingsList["use_rich_punc"] == 1):
            self.richPunc.select()
        else:
            self.richPunc.deselect()

        self.detectionLangs.delete("1.0", tkinter.END)
        detectionLangsListStr = str(self.settingsList["detection_languages"])
        detectionLangsListStr = detectionLangsListStr.replace('[', '').replace(']', '').replace("'", '')
        self.detectionLangs.insert(tkinter.END, detectionLangsListStr)

        self.recordTime.set(self.settingsList["max_record_len"])
        self.maxToken.set(self.settingsList["max_token"])

    def openSettings(self):
        self.settingsWindow = customtkinter.CTkToplevel(self.basis)
        self.settingsWindow.title("Settings")
        self.settingsWindow.grid_rowconfigure(0, weight=1)
        self.settingsWindow.grid_columnconfigure(0, weight=1)
        self.settingsWindow.geometry(str(self.uiMargins.appSizeX) + "x" + "640")
        self.settingsWindow.resizable(width=False, height=True)

        self.settingsMainframe = customtkinter.CTkScrollableFrame(self.settingsWindow)
        self.settingsMainframe.grid(row=0, column=0, sticky="nsew")
        self.settingsMainframe.grid_rowconfigure(0, weight=1)

        #Language
        self.languageSelectionFrame = customtkinter.CTkFrame(self.settingsMainframe)
        self.languageSelectionFrame.pack(fill="x", expand=True, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.languageSelectionDesc = customtkinter.CTkLabel(self.languageSelectionFrame, text=locale.data["settings_languages"])
        self.languageSelectionDesc.pack(side = 'left')
        self.languageSelection = customtkinter.CTkOptionMenu(self.languageSelectionFrame, values=languageList)
        self.languageSelection.pack(side = 'right')

        #Recognition Method
        self.modelSelectionFrame = customtkinter.CTkFrame(self.settingsMainframe)
        self.modelSelectionFrame.pack(fill="x", expand=True, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.modelSelectionDesc = customtkinter.CTkLabel(self.modelSelectionFrame, text=locale.data["settings_model"])
        self.modelSelectionDesc.pack(side = 'left')
        self.modelSelection = customtkinter.CTkOptionMenu(self.modelSelectionFrame, values=["ChatGPT"])
        self.modelSelection.pack(side = 'right')

        #API Key
        self.apiKeyFrame = customtkinter.CTkFrame(self.settingsMainframe)
        self.apiKeyFrame.pack(fill="x", expand=True, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.apiKeyDesc = customtkinter.CTkLabel(self.apiKeyFrame, text=locale.data["settings_apikey"], justify= "left")
        self.apiKeyDesc.pack(side = 'left')
        self.apiKey = customtkinter.CTkTextbox(self.apiKeyFrame, height=80)
        self.apiKey.pack(side = 'right')

        #Rich Punct Method
        self.richPuncFrame = customtkinter.CTkFrame(self.settingsMainframe)
        self.richPuncFrame.pack(fill="x", expand=True, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.richPuncDesc = customtkinter.CTkLabel(self.richPuncFrame, text=locale.data["settings_richpunct"])
        self.richPuncDesc.pack(side = 'left')
        self.richPunc = customtkinter.CTkCheckBox(self.richPuncFrame, text="")
        self.richPunc.pack(side = 'right')

        #Detection Languages Method
        self.detectionLangsFrame = customtkinter.CTkFrame(self.settingsMainframe)
        self.detectionLangsFrame.pack(fill="x", expand=True, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.detectionLangsDesc = customtkinter.CTkLabel(self.detectionLangsFrame, text=locale.data["settings_detectionlangs"], justify= "left")
        self.detectionLangsDesc.pack(side = 'left')
        self.detectionLangs = customtkinter.CTkTextbox(self.detectionLangsFrame, height=80)
        self.detectionLangs.pack(side = 'right')

        #Detected Languages List
        self.supportedDetectLangsFrame = customtkinter.CTkFrame(self.settingsMainframe)
        self.supportedDetectLangsFrame.pack(fill="x", expand=True, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.supportedDetectLangsDesc = customtkinter.CTkLabel(self.supportedDetectLangsFrame, text=locale.data["settings_detectionlangs_support"])
        self.supportedDetectLangsDesc.pack(side = 'left')

        def opensupportedDetectLangs():
            url = "https://platform.openai.com/docs/guides/speech-to-text/supported-languages"
            webbrowser.open(url)
        self.supportedDetectLangs = customtkinter.CTkButton(master=self.supportedDetectLangsFrame, text=locale.data["settings_visit"], command=opensupportedDetectLangs)
        self.supportedDetectLangs.pack(side='right')

        #Max Record Time
        self.recordTimeFrame = customtkinter.CTkFrame(self.settingsMainframe)
        self.recordTimeFrame.pack(fill="x", expand=True, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.recordTimeDesc = customtkinter.CTkLabel(self.recordTimeFrame, text=locale.data["settings_maxrecordlen"])
        self.recordTimeDesc.pack(side = 'left')

        self.recordTimeVar = customtkinter.StringVar(master = self.settingsWindow, value = self.settingsList["max_record_len"])
        def recordTimerVarChange(value):
            self.recordTimeVar.set(str(value))

        self.recordTime = customtkinter.CTkSlider(self.recordTimeFrame, from_=20, to=120, number_of_steps=20, command=recordTimerVarChange)
        self.recordTime.pack(side='right')
        self.recordTimeVar.set(str(self.recordTime.get())) #initialize
        self.recordTimeShowDesc = customtkinter.CTkLabel(self.recordTimeFrame, textvariable=self.recordTimeVar)
        self.recordTimeShowDesc.pack(side='right')

        #Max Token Usage
        self.maxTokenFrame = customtkinter.CTkFrame(self.settingsMainframe)
        self.maxTokenFrame.pack(fill="x", expand=True, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.maxTokenDesc = customtkinter.CTkLabel(self.maxTokenFrame, text=locale.data["settings_maxtoken"])
        self.maxTokenDesc.pack(side = 'left')

        self.maxTokenVar = customtkinter.StringVar(master = self.settingsWindow, value = self.settingsList["max_token"])
        def maxTokenrVarChange(value):
            self.maxTokenVar.set(str(value))

        self.maxToken = customtkinter.CTkSlider(self.maxTokenFrame, from_=100, to=500, number_of_steps=8, command=maxTokenrVarChange)
        self.maxToken.pack(side='right')
        self.maxTokenVar.set(str(self.maxToken.get())) #initialize
        self.maxTokenShowDesc = customtkinter.CTkLabel(self.maxTokenFrame, textvariable=self.maxTokenVar)
        self.maxTokenShowDesc.pack(side='right')

        #Github informations
        self.repoInfoFrame = customtkinter.CTkFrame(self.settingsMainframe)
        self.repoInfoFrame.pack(fill="x", expand=True, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.repoInfoDesc = customtkinter.CTkLabel(self.repoInfoFrame, text=locale.data["settings_info_repo"])
        self.repoInfoDesc.pack(side = 'left')

        def openRepoInfo():
            url = "https://github.com/urbanmaid/Stenoid_stt"
            webbrowser.open(url)

        self.repoInfo = customtkinter.CTkButton(master=self.repoInfoFrame, text=locale.data["settings_visit"], command=openRepoInfo)
        self.repoInfo.pack(side='right')
    
        #Project Documents informations
        self.projectDocuFrame = customtkinter.CTkFrame(self.settingsMainframe)
        self.projectDocuFrame.pack(fill="x", expand=True, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.projectDocuDesc = customtkinter.CTkLabel(self.projectDocuFrame, text=locale.data["settings_info_project"])
        self.projectDocuDesc.pack(side = 'left')

        def openprojectDocu():
            url = "https://sun-moonflower-1cc.notion.site/SW-320bec5e39f24f4ea594fa3247411583"
            webbrowser.open(url)

        self.projectDocu = customtkinter.CTkButton(master=self.projectDocuFrame, text=locale.data["settings_visit"], command=openprojectDocu)
        self.projectDocu.pack(side='right')

        #information
        self.projectInfoFrame = customtkinter.CTkFrame(self.settingsMainframe)
        self.projectInfoFrame.pack(fill="x", expand=True, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.projectInfoDesc = customtkinter.CTkLabel(self.projectInfoFrame, text="Stenoid v."+versioninfo+"\nTranslation of this program may not be correct.", justify= "left")
        self.projectInfoDesc.pack(side = 'left')

        #Save Settings
        self.buttonSave = customtkinter.CTkButton(master=self.settingsWindow, text="Save", command=self.saveSettings)
        self.buttonSave.grid(row=1, column=0, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.labelSaveNotifier = customtkinter.CTkLabel(master=self.settingsWindow, text=locale.data["save_warning"])
        self.labelSaveNotifier.grid(row=2, column=0, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)

        self.loadSettings()

    def saveSettings(self):
        self.settingsList["language"] = self.languageSelection.get()
        self.settingsList["api_key"] = self.apiKey.get("1.0", tkinter.END)
        self.settingsList["use_rich_punc"] = self.richPunc.get()
        detectionLangsListStr = self.detectionLangs.get("1.0", tkinter.END)
        detectionLangsList = [langs.strip() for langs in detectionLangsListStr.split(',')]
        self.settingsList["detection_languages"] = detectionLangsList
        self.settingsList["max_record_len"] = self.recordTime.get()
        self.settingsList["max_token"] = self.maxToken.get()

        global json_string
        json_string = json.dumps(self.settingsList, indent=4)
        with open(settings_file, 'w') as json_file:
            json_file.write(json_string)
