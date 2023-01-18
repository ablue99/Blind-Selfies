import cv2
import numpy as np
import pyaudio
import pyttsx3
import speech_recognition as sr

computer = pyttsx3.init()
r = sr.Recognizer()

computer.say("Specify a position your face should appear in the selfie, or ask for a list of "
             + "positions by simply stating list.")
computer.runAndWait()

def command_menu():
    computer = pyttsx3.init()
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=2)

            computer.say("Specify a position your face should appear in the selfie, or ask for a list of "
                         + "positions by simply stating list. Speak now!")
            computer.runAndWait()
            audio = r.listen(source)
        try:
            print("You said " + r.recognize_google(audio))
            quad = r.recognize_google(audio);
            quad = str.lower(quad)
            if quad == "list":
                computer.say("The list options are: top left, top right, bottom left, and bottom right")
                computer.runAndWait()
            elif quad in {"top left", "top right", "bottom left", "bottom right"}:
                computer.say("Selected " + quad + ".")
                computer.runAndWait()
                break
            else:
                computer.say("Could not understand audio.")
                computer.runAndWait()

        except sr.UnknownValueError:
            computer.say("Could not understand audio.")
            computer.runAndWait()
    return quad

quad_command = command_menu()

