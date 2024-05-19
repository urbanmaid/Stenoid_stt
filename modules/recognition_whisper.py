import whisper
import ffmpeg

modelSizeList = ["base", "small", "medium"]

class RecognizerWhisper():
    def __init__(self, modelSize):
        if modelSize in modelSizeList:
            self.modelSize = modelSize
        else:
            print("The model Definition is invalid. Set as basic model for recognition.")
            self.modelSize = "base"
        self.model = whisper.load_model(self.modelSize)

    def Convert(self, audioSource):
        audioFile = whisper.load_audio(audioSource)
        result = self.model.transcribe(audioFile)
        return result['text']