import json
import os
import whisper
import openai
import ffmpeg

from modules.locales import LocaleManager

modelSizeList = ["base", "small", "medium"]
with open('language_map.json', 'r', encoding='utf-8') as f:
    language_map_table = json.load(f)
with open('settings.json', 'r', encoding='utf-8') as g:
    settings = json.load(g)
keyTemp = (settings["api_key"])
keyTemp = keyTemp.replace("\n", '')
openai.api_key = keyTemp #this is my key so others cannot use this one.
locale = LocaleManager()

class RecognizerWhisper():
    def __init__(self, modelSize):
        if modelSize in modelSizeList:
            self.modelSize = modelSize
        else:
            print("The model Definition is invalid. Set as basic model for recognition.")
            self.modelSize = "base"
        self.model = whisper.load_model(self.modelSize)

    def Convert(self, audioSource, language):
        audioFile = whisper.load_audio(audioSource)
        if (language=="Auto"):
            result = self.model.transcribe(audioFile)
        else:
            language_code = language_map_table[language]
            if (language_code == None):
                result = self.model.transcribe(audioFile)
            else:
                result = self.model.transcribe(audioFile, language=language_code)
        return result['text']

    def GramFix(self, text, richpunc):
        if (richpunc == 1):
            msgcontent = f"{locale.data["gpt_request_gramfix_desc"]} {locale.data["gpt_request_gramfix_richpunc"]} \n \"{text}\""
        else:
            msgcontent = f"{locale.data["gpt_request_gramfix_desc"]} \n \"{text}\""
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": locale.data["gpt_request_gramfix_intro"]},
                {"role": "user", "content": msgcontent}
            ],
            max_tokens=int(settings["max_token"]),
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content