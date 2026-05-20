import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import pywhatkit
import pyautogui
import wikipedia
import os

recognizer = sr.Recognizer()

# Voice setup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # female voice
engine.setProperty('rate', 170)

def speak(text):
    print("Jarvis:", text)
    engine.stop()
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        return recognizer.recognize_google(audio).lower()

def processCommand(command):
    print("You said:", command)

    if "exit" in command or "shutdown jarvis" in command:
        speak("Goodbye Zunair")
        exit()

    elif "sleep" in command:
        speak("Going to sleep mode")
        return "sleep"

    elif "wake up" in command:
        speak("I am active again")
        return "wake"

    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "open vscode" in command:
        speak("Opening Visual Studio Code")
        os.system("code")

    elif "play" in command:
        song = command.replace("play", "")
        speak("Playing " + song)
        pywhatkit.playonyt(song)

    elif "time" in command:
        time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {time}")

    # 🔥 SMART WIKIPEDIA
    elif "who is" in command or "what is" in command or "tell me about" in command:
        speak("Searching Wikipedia")
        topic = command.replace("who is", "").replace("what is", "").replace("tell me about", "").strip()

        try:
            result = wikipedia.summary(topic, sentences=2)
            speak(result)
        except:
            speak("Sorry, I could not find information")

    else:
        speak("I did not understand")

    return "active"


if __name__ == "__main__":

    speak("Hello Zunair, Jarvis is ready ")

    active = False

    while True:
        try:
            command = listen()

            # Wake word
            if "jarvis" in command:
                speak("Yes, I am listening")
                active = True
                continue

            if active:
                state = processCommand(command)

                if state == "sleep":
                    active = False

        except sr.WaitTimeoutError:
            print("Timeout...")

        except sr.UnknownValueError:
            print("Could not understand")

        except sr.RequestError:
            print("Internet error")

        except Exception as e:
            print("Error:", e)