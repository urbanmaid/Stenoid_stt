import asyncio
import numpy as np
import os
import pyaudio
import wave

def amplify_record(data, factor):
    numpydata = np.frombuffer(data, dtype=np.int16)
    numpydata = numpydata * factor
    numpydata = np.clip(numpydata, -32768, 32767)
    return numpydata.tobytes()

class Recorder:
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.frames = []
        self.VOLUME = 3

        self.OPT_DIR = os.path.dirname(os.path.realpath(__file__))
        self.OPT_NAME = "output.mp3"
        self.WAVE_OUTPUT_FILENAME = os.path.join(self.OPT_DIR, self.OPT_NAME)

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False

    async def start_record(self):
        self.is_recording = True
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                      rate=self.RATE, input=True,
                                      frames_per_buffer=self.CHUNK)
        self.frames = []
        print("녹음을 시작합니다.")

    async def record(self):
        while self.is_recording:
            data = self.stream.read(self.CHUNK, exception_on_overflow = False)
            self.frames.append(data)
            await asyncio.sleep(0)  # 현재 태스크를 양보하여 다른 비동기 작업이 실행될 수 있도록 합니다.

    async def pause_record(self):
        self.is_recording = False

    async def resume_record(self):
        self.is_recording = True

    async def stop_record(self):
        self.is_recording = False

        self.stream.stop_stream()
        self.stream.close()

        amplified_frames = []
        for data in self.frames:
            amplified_data = amplify_record(data, self.VOLUME)
            amplified_frames.append(amplified_data)

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(amplified_frames))
        wf.close()

        print("녹음이 완료되었습니다.")

    async def dispose_record(self):
        self.is_recording = False
        
        self.stream.stop_stream()
        self.stream.close()
        self.frames = []
        print("녹음이 중지되었습니다.")