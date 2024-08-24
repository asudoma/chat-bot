import time

import speech_recognition as sr


def main():
    r = sr.Recognizer()
    start = time.time()
    with sr.AudioFile("stih.wav") as source:
        audio_data = r.record(source)
        text = r.recognize_whisper(audio_data)
        print(text)
    end = time.time()
    print(end - start)
