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
    def __init__(self, outputDir, outputName):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.frames = []
        self.VOLUME = 1
        #self.rms_threshold = 80

        self.OPT_DIR = outputDir
        self.OPT_NAME = outputName
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
            try:
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                self.frames.append(data)

                '''
                numpydata = np.frombuffer(data, dtype=np.int16)
                rms = np.sqrt(np.mean(numpydata**2))
                #print(f"Current RMS level: {rms}")
                if rms < self.rms_threshold:
                    print("입력 없음")
                '''
            except Exception as e:
                print(f"Error reading stream data: {e}")
            await asyncio.sleep(0)  # 현재 태스크를 양보하여 다른 비동기 작업이 실행될 수 있도록 합니다.

    async def pause_record(self):
        self.is_recording = False

    async def resume_record(self):
        self.is_recording = True

    async def stop_record(self):
        try:
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
        except Exception as e:
            print(f"Error stopping record: {e}")


    async def dispose_record(self):
        self.is_recording = False
        
        self.stream.stop_stream()
        self.stream.close()
        self.frames = []
        print("녹음이 중지되었습니다.")