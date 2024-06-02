import asyncio
import customtkinter
import os
import threading
import tkinter
import pyperclip
import time

from modules.audio_recorder import Recorder
from modules.ui_margins import UIMargins
from modules.recognition_whisper import RecognizerWhisper
from modules.locales import LocaleManager

# update for backup

# Default Options
#root = tkinter.Tk()
settingsWindow = ""

# Module and Class Definition
optName = "output.mp3"
fixedText = ""

# Module loader
recorder = Recorder(outputDir = os.path.dirname(os.path.realpath(__file__)), outputName = optName)
recognizerW = RecognizerWhisper(modelSize = "base")
uiMargins = UIMargins()
event = asyncio.Event()
locale = LocaleManager()

isPaused = False
usingsettingWin = False
RECORD_SECONDS = 20

async def do_record():
    await recorder.start_record()  # 녹음 시작
    task = asyncio.create_task(recorder.record())  # 별도의 태스크로 녹음 시작
    await asyncio.sleep(RECORD_SECONDS)  # 녹음 시간만큼 대기
    await recorder.stop_record()  # 녹음 멈추고 파일로 저장
    print("Start Recording")

def do_record_sync():
    asyncio.run(do_record())

def do_record_thread():
    threading.Thread(target=do_record_sync, daemon=True).start()
    stringVarStatus.set(locale.data["status_recording"])
    stringVarStatusAux.set(locale.data["statusaux_recording"])

async def stop_record():
    if recorder.is_recording:
        await recorder.stop_record()
    textTarget = recognizerW.Convert("output.mp3")
    print(textTarget)
    print("Stop Recording")
    resultTextbox.insert(tkinter.END, textTarget)

def stop_record_sync(loop):
    asyncio.run_coroutine_threadsafe(stop_record(), loop)

def stop_record_thread():
    loop = asyncio.get_event_loop()
    threading.Thread(target=stop_record_sync, args=(loop,), daemon=True).start()
    stringVarStatus.set(locale.data["status_idle"])
    stringVarStatusAux.set(locale.data["statusaux_idle"])

# Pause Record
async def pause_record():
    await recorder.pause_record()
    print("Pause Recording")
    stringVarStatus.set(locale.data["status_paused"])
    stringVarStatusAux.set(locale.data["statusaux_paused"])

# Resume Record
async def resume_record():
    await recorder.resume_record()
    print("Resume Recording")
    stringVarStatus.set(locale.data["status_recording"])
    stringVarStatusAux.set(locale.data["statusaux_recording"])

def pause_resume_control_thread():
    if (isPaused == False):
        isPaused = True
        threading.Thread(target=asyncio.run(stop_record()), daemon=True).start()
    else:
        isPaused = False
        threading.Thread(target=(asyncio.run(resume_record())), daemon=True).start()

def gram_fix():
    fixedText = (recognizerW.GramFix(resultTextbox.get("1.0", tkinter.END)))
    resultTextbox.delete("1.0", tkinter.END)
    resultTextbox.insert(tkinter.END, fixedText)
    # print(fixedText)

def open_settings():
    global usingsettingWin
    if (usingsettingWin == False):
        usingsettingWin = True
        settingsWindow = customtkinter.CTkToplevel(app)
        settingsWindow.title("Settings")

def discard_result():
    resultTextbox.delete("1.0", tkinter.END)

def copy_converted_text():
    pyperclip.copy(resultTextbox.get("1.0", tkinter.END))
    stringVarStatus.set(locale.data["status_copied"])
    stringVarStatusAux.set(locale.data["statusaux_copied"])
    time.sleep(1)
    stringVarStatus.set(locale.data["status_idle"])
    stringVarStatusAux.set(locale.data["statusaux_idle"])

# UI Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.geometry(str(uiMargins.appSizeX) + "x" + str(uiMargins.appSizeY))
app.resizable(width=False, height=False)
stringVarStatus = customtkinter.StringVar(master = app, value = "Idle")
stringVarStatusAux = customtkinter.StringVar(master = app, value = "Tap Record to start record.")
stringVarStatus.set(locale.data["status_idle"])
stringVarStatusAux.set(locale.data["statusaux_idle"])

main = customtkinter.CTkFrame(master = app)
main.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

resultTextbox = customtkinter.CTkTextbox(master = main, width = (uiMargins.appSizeX - uiMargins.frameMargin), height = 80, font = ('Arial', uiMargins.textSizeResult, 'normal'))
#resultTextbox.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
resultTextbox.pack()

mainFrame = customtkinter.CTkFrame(master = main)
#mainFrame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
mainFrame.pack()

# left
leftFrame = customtkinter.CTkFrame(master = mainFrame)
leftFrame.pack(side = 'left')

buttonRec = customtkinter.CTkButton(master=leftFrame, text=locale.data["button_record"], command=do_record_thread)
buttonRec.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

buttonPause = customtkinter.CTkButton(master=leftFrame, text=locale.data["button_pause"], command=pause_resume_control_thread)
buttonPause.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

buttonStop = customtkinter.CTkButton(master=leftFrame, text=locale.data["button_stop"], command=stop_record_thread)
buttonStop.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

buttonLanguages = customtkinter.CTkButton(master=leftFrame, text=locale.data["button_languages"], command=stop_record_thread)
buttonLanguages.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

# center
centerFrame = customtkinter.CTkFrame(master = mainFrame, fg_color = 'transparent')
centerFrame.pack(side = 'left')

labelStatus = customtkinter.CTkLabel(master = centerFrame, textvariable = stringVarStatus, font = ('Arial', uiMargins.textSizeStatus, 'bold'), width = 200, fg_color="transparent")
labelStatus.pack()

labelStatusAux = customtkinter.CTkLabel(master = centerFrame, textvariable = stringVarStatusAux, fg_color="transparent")
labelStatusAux.pack()

# right
rightFrame = customtkinter.CTkFrame(master = mainFrame)
rightFrame.pack(side = 'left')

buttonGram = customtkinter.CTkButton(master=rightFrame, text=locale.data["button_fix"], command=gram_fix)
buttonGram.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

buttonPunc = customtkinter.CTkButton(master=rightFrame, text=locale.data["button_settings"], command=open_settings)
buttonPunc.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

buttonDiscard = customtkinter.CTkButton(master=rightFrame, text=locale.data["button_discard"], command=discard_result)
buttonDiscard.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

buttonInput = customtkinter.CTkButton(master=rightFrame, text=locale.data["button_input"], command=copy_converted_text)
buttonInput.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

def main():
    app.mainloop()

if __name__ == "__main__":
    main()
