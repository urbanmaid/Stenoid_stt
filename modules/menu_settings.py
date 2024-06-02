import customtkinter
import json
import os
import tkinter

#app = customtkinter.CTk()
buttonRec = customtkinter.CTkButton(master=settingsWindow, text="Record")

class Settings:
    def __init__(self, basis):
        self.settingsWindow = ""
        self.basis = basis

    def openSettings(self):
        self.settingsWindow = customtkinter.CTkToplevel()
        self.settingsWindow.title("Settings")

    # def settingMenus(self):

