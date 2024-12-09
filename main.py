import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import subprocess
import webbrowser
import random
import signal
import psutil

def speak(text):
    tts = gTTS(text)
    filename = "response.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is unavailable right now.")
            return ""

def open_application(app_name):
    try:
        speak(f"Opening {app_name}")
        subprocess.Popen([app_name])  # Use Popen to run the command without blocking
    except FileNotFoundError:
        speak(f"Sorry, I couldn't find the application named {app_name}.")
    except Exception as e:
        speak(f"An error occurred while opening {app_name}: {str(e)}")

def close_application(app_name):
    try:
        speak(f"Closing {app_name}")
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == app_name.lower():
                os.kill(proc.info['pid'], signal.SIGTERM)
                speak(f"{app_name} has been closed.")
                return
        speak(f"Sorry, I couldn't find any running process for {app_name}.")
    except Exception as e:
        speak(f"An error occurred while closing {app_name}: {str(e)}")

def tell_joke():
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "Why couldn’t the bicycle stand up by itself? It was two-tired.",
        "What do you call fake spaghetti? An impasta!",
        "Why don’t some couples go to the gym? Because some relationships don’t work out."
    ]
    joke = random.choice(jokes)
    speak(joke)

def process_command(command):
    print(f"Debug: Recognized command: {command}")
    if "open" in command:
        app_name = command.replace("open", "").strip()
        open_application(app_name)
    elif "close" in command:
        app_name = command.replace("close", "").strip()
        close_application(app_name)
    elif "search for" in command:
        query = command.replace("search for", "").strip()
        speak(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "how are you" in command:
        speak("I'm just a program, but I'm doing well. How can I assist you?")
    elif "hello" in command:
        speak("Hello! How can I assist you?")
    elif "tell me a joke" in command:
        tell_joke()
    elif "stop" in command or "exit" in command or "goodbye" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I didn't understand that. Can you try again?")

def main():
    speak("Hello, user! How may I help you?")
    while True:
        command = listen()
        if command:
            process_command(command)

if __name__ == "__main__":
    main()
