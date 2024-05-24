import json
import os

import speech_recognition as sr
from langchain_community.llms import Ollama
from gtts import gTTS

llm = Ollama(model="llama3")
recognizer = sr.Recognizer()
microphone = sr.Microphone()


def recognize_speech():
    try:
        print("A moment of silence, please...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
        print("You can speak now!")
        with microphone as source:
            audio = recognizer.listen(source)
        print("Recognizing the prompt...")
        try:
            value = json.loads(recognizer.recognize_vosk(audio))["text"]
            print("You said {}".format(value))
            return value
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
            return ""
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
            return ""
    except KeyboardInterrupt:
        pass
        return ""


def query_llm(prompt):
    return llm.invoke(prompt)


def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")
    os.system("mpg123 output.mp3")


def handle_dialogue():
    while True:
        user_input = recognize_speech()
        if user_input.lower() in ["bye bye"]:
            speak("Goodbye!")
            break
        # response = query_llm(user_input)
        # speak(response)

        sent = ""
        for chunks in llm.stream(user_input):
            sent += chunks
            if chunks == "." or chunks == "!" or chunks == "?":
                speak(sent)
                sent = ""


def detect_wake_word(wake_word="hey boss"):
    while True:
        text = recognize_speech()
        if wake_word in text.lower():
            speak("Hi! How can I help you?")
            handle_dialogue()


if __name__ == "__main__":
    detect_wake_word()
