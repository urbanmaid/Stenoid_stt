import whisper

modelSizeList = ["base", "small", "medium"]

class RecognizerWhisper():
    def __init__(self, modelSize):
        self.modelSize = modelSize
        self.model = whisper.load_model(self.modelSize)
    def Convert(self, audioSource):
        result = self.model.transcribe(audioSource)
        return result['text']