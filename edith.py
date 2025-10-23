import speech_recognition as sr  # type: ignore
import pyttsx3  # pyright: ignore[reportMissingImports]
import datetime
import wikipedia  # pyright: ignore[reportMissingImports]
import webbrowser
import os
import time

print('Loading Edith...')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # ✅ Fixed: correct getProperty/setProperty usage


def speak(text: str) -> None:
    """Make Edith speak a given text"""
    engine.say(text)
    engine.runAndWait()


def wishMe():
    """Greet the user based on the current time"""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")


def takeCommand() -> str:
    """Take microphone input from the user and return recognized text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Recognizing...")
            statement = r.recognize_google(audio, language='en-in')
            print(f"User said: {statement}\n")
        except Exception:
            speak("I didn't hear you, please say that again.")
            return "none"
        return statement.lower()


if __name__ == '__main__':
    speak("Loading Edith...")
    wishMe()

    while True:
        speak("What can I do for you?")
        statement = takeCommand()

        if statement == "none" or not statement.strip():
            continue

        if any(phrase in statement for phrase in ["good bye", "okay bye", "turn off"]):
            speak("See you later!")
            break

        elif 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            try:
                results = wikipedia.summary(statement, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception:
                speak("Sorry, I couldn't find anything on Wikipedia.")

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://youtube.com")
            speak("YouTube is now open.")
            time.sleep(3)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google Chrome is open now.")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("https://mail.google.com")
            speak("Google Mail is open now.")
            time.sleep(5)
            
        elif 'open veeam' in statement:
            webbrowser.open_new_tab("veeam.com")
            speak("veeam is open now.")
            time.sleep(5)
            
        elif 'open the business' in statement:
            webbrowser.open_new_tab("topsocalproperties.com")
            speak("open now.")
            time.sleep(5)
            
        elif 'open amazon' in statement:
            webbrowser.open_new_tab("amazon.com")
            speak("amazon open.")
            time.sleep(5)
            
       