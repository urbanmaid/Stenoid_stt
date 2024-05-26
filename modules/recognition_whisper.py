import os
import whisper
import openai
import ffmpeg

modelSizeList = ["base", "small", "medium"]
openai.api_key = os.getenv('OPENAI_APIKEY') #this is my key so others cannot use this one.

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

    def GramFix(self, text):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0301",
            messages=[
                {"role": "system", "content": "This is a service for fixing grammar and punctuation."},
                {"role": "user", "content": f"Fix the grammar and punctuation of this sentence, without Language Changes: \"{text}\""}
            ],
            max_tokens=250,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content