import customtkinter
import json
import os
import tkinter

from modules.ui_margins import UIMargins

#app = customtkinter.CTk()

class Settings:
    def __init__(self, basis):
        self.settingsWindow = ""
        self.basis = basis
        self.uiMargins = UIMargins()

    def openSettings(self):
        self.settingsWindow = customtkinter.CTkToplevel(self.basis)
        self.settingsWindow.title("Settings")
        self.settingsWindow.grid_rowconfigure(0, weight=1)
        self.settingsWindow.grid_columnconfigure(0, weight=1)
        self.settingsWindow.geometry(str(self.uiMargins.appSizeX) + "x" + str(self.uiMargins.appSizeY))
        self.settingsWindow.resizable(width=True, height=False)

        self.settingsMainframe = customtkinter.CTkScrollableFrame(self.settingsWindow)
        self.settingsMainframe.grid(row=0, column=0, sticky="nsew")
        self.settingsMainframe.grid_rowconfigure(0, weight=1)

        self.languageSelectionFrame = customtkinter.CTkFrame(self.settingsMainframe)
        self.languageSelectionFrame.pack(fill="x", expand=True, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.languageSelectionDesc = customtkinter.CTkLabel(self.languageSelectionFrame, text="Languages")
        self.languageSelectionDesc.pack(side = 'left')
        self.languageSelection = customtkinter.CTkOptionMenu(self.languageSelectionFrame, values=val_language)
        self.languageSelection.pack(side = 'right')

        self.modelSelectionFrame = customtkinter.CTkFrame(self.settingsMainframe)
        self.modelSelectionFrame.pack(fill="x", expand=True, padx = self.uiMargins.btnMargin, pady = self.uiMargins.btnMargin)
        self.modelSelectionDesc = customtkinter.CTkLabel(self.modelSelectionFrame, text="Recognition Model")
        self.modelSelectionDesc.pack(side = 'left')
        self.modelSelection = customtkinter.CTkOptionMenu(self.modelSelectionFrame, values=["option 1", "option 2"])
        self.modelSelection.pack(side = 'right')

        #self.buttonTest = customtkinter.CTkButton(master=self.settingsMainframe, text="Test Button")
        #self.buttonTest.pack()
    # def settingMenus(self):

