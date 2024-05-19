import asyncio
import tkinter
import customtkinter
from audio_recorder import Recorder
from ui_margins import UIMargins
import threading

# Default Options
root = tkinter.Tk()
stringVarStatus = tkinter.StringVar(master = root)
stringVarStatus.set("Idle")
stringVarStatusAux = tkinter.StringVar(master = root)
stringVarStatusAux.set("Tap Record To do record.")

# Module and Class Definition
recorder = Recorder()
uiMargins = UIMargins()
event = asyncio.Event()

isPaused = False
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
    stringVarStatusAux.set("Tap Stop to convert to text.")

async def stop_record():
    await recorder.stop_record()
    print("Stop Recording")

def stop_record_sync():
    asyncio.run(stop_record())

def stop_record_thread():
    threading.Thread(target=stop_record_sync, daemon=True).start()
    stringVarStatusAux.set("Tap Record To do record.")


# Pause Record
async def pause_record():
    await recorder.pause_record()
    print("Pause Recording")

# Resume Record
async def resume_record():
    await recorder.resume_record()
    print("Resume Recording")

def pause_resume_control_thread():
    if (isPaused == False):
        isPaused = True
        threading.Thread(target=asyncio.run(stop_record()), daemon=True).start()
    else:
        isPaused = False
        threading.Thread(target=(asyncio.run(resume_record())), daemon=True).start()

# UI Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.geometry("600x240")
app.resizable(width=False, height=False)

mainFrame = customtkinter.CTkFrame(master = app)
mainFrame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

# left
leftFrame = customtkinter.CTkFrame(master = mainFrame)
leftFrame.pack(side = 'left')

buttonRec = customtkinter.CTkButton(master=leftFrame, text="Record", command=do_record_thread)
buttonRec.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

buttonPause = customtkinter.CTkButton(master=leftFrame, text="Pause", command=pause_resume_control_thread)
buttonPause.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

buttonStop = customtkinter.CTkButton(master=leftFrame, text="Stop", command=stop_record_thread)
buttonStop.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

buttonLanguages = customtkinter.CTkButton(master=leftFrame, text="Languages", command=stop_record_thread)
buttonLanguages.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

# center
centerFrame = customtkinter.CTkFrame(master = mainFrame, fg_color = 'transparent')
centerFrame.pack(side = 'left')

labelStatus = customtkinter.CTkLabel(master = centerFrame, textvariable = stringVarStatus, font = ('Arial', 22, 'bold'), width = 200, fg_color="transparent")
labelStatus.pack()

labelStatusAux = customtkinter.CTkLabel(master = centerFrame, textvariable = stringVarStatusAux, fg_color="transparent")
labelStatusAux.pack()

# right
rightFrame = customtkinter.CTkFrame(master = mainFrame)
rightFrame.pack(side = 'left')

buttonGram = customtkinter.CTkButton(master=rightFrame, text="Grammar Fix", command=do_record_thread)
buttonGram.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

buttonPunc = customtkinter.CTkButton(master=rightFrame, text="Punc Fix", command=pause_resume_control_thread)
buttonPunc.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

buttonDiscard = customtkinter.CTkButton(master=rightFrame, text="Discard", command=stop_record_thread)
buttonDiscard.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

buttonInput = customtkinter.CTkButton(master=rightFrame, text="Input", command=stop_record_thread)
buttonInput.pack(padx = uiMargins.btnMargin, pady = uiMargins.btnMargin)

def main():
    app.mainloop()

if __name__ == "__main__":
    main()
