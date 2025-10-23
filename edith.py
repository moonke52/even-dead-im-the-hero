

       

import speech_recognition as sr  # type: ignore
import pyttsx3  # pyright: ignore[reportMissingImports]
import datetime
import wikipedia  # pyright: ignore[reportMissingImports]
import webbrowser
import os
import time
import threading
import wolframalpha  # pip install wolframalpha
import tkinter as tk
from tkinter import ttk, scrolledtext
import openai  # pip install openai
import random

# === User Name ===
USER_NAME = "Hudson"

# === OpenAI API Key ===
openai.api_key = "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"

# === WolframAlpha Setup ===
APP_ID = "RL2H7JW94V"
client = wolframalpha.Client(APP_ID)

# === Voice Engine Setup ===
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('volume', 1.0)

# === GUI Chat Window ===
class ChatWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Edith Chat")
        self.window.geometry("600x450")
        self.chat_area = scrolledtext.ScrolledText(
            self.window,
            wrap=tk.WORD,
            font=("Helvetica", 12),
            bg="black",
            fg="white"
        )
        self.chat_area.pack(expand=True, fill='both')
        self.chat_area.config(state=tk.DISABLED)
    
    def insert_user(self, text):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"You: {text}\n", 'user')
        self.chat_area.tag_config('user', foreground='red')
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)
    
    def insert_edith(self, text):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"Edith: {text}\n", 'edith')
        self.chat_area.tag_config('edith', foreground='blue')
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)
        engine.say(text)
        engine.runAndWait()

chat = ChatWindow()

# === Speak function ===
def speak(text: str):
    chat.insert_edith(text)

# === Greeting ===
def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak(f"Good morning, {USER_NAME}!")
    elif 12 <= hour < 18:
        speak(f"Good afternoon, {USER_NAME}!")
    else:
        speak(f"Good evening, {USER_NAME}!")

# === Math Popup ===
def show_math_popup(question: str, answer: str):
    window = tk.Toplevel()
    window.title("Edith Math Answer")
    window.geometry("400x200")
    window.configure(bg="#1E1E1E")
    window.attributes("-topmost", True)

    ttk.Label(
        window,
        text=f"Problem:\n{question}",
        font=("Helvetica", 16, "bold"),
        foreground="#FFD700",
        background="#1E1E1E",
        anchor="center",
        justify="center"
    ).pack(pady=(20,10))

    ttk.Label(
        window,
        text=f"Answer:\n{answer}",
        font=("Helvetica", 20, "bold"),
        foreground="#00FF00",
        background="#1E1E1E",
        anchor="center",
        justify="center"
    ).pack(pady=(10,20))

    window.after(5000, window.destroy)
    window.mainloop()

# === Rainbow Parrot Easter Egg ===
def rainbow_parrot():
    parrot = r"""
          ▄████▄
         ▄█▀▀▀▀█▄
        █▀     ▀█
        █  ◕ ◕  █
        █   ▀   █
        ▀█▄   ▄█▀
          ▀████▀
    """
    speak("Here's a rainbow parrot for you, Hudson!")
    chat.insert_edith(parrot)

# === Dynamic AI Small Talk using GPT with guaranteed fallback ===
conversation_history = []

fallback_responses = [
    "Hmm, I'm not sure about that, but I'm learning!",
    "I wish I could answer that, Hudson!",
    "Here's a fun fact: The first computer bug was a real moth!",
    "Why did the computer show up at work late? It had a hard drive!",
    "I would love to chat more, but I'm still learning!"
]

def handle_small_talk(statement):
    try:
        conversation_history.append(f"You: {statement}")
        prompt = "\n".join(conversation_history) + "\nEdith:"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        answer = response.choices[0].text.strip()
        conversation_history.append(f"Edith: {answer}")
        speak(answer)
    except Exception as e:
        print("GPT Error:", e)  # Log error in terminal
        fallback = random.choice(fallback_responses)
        speak(fallback)

# === Command Processor ===
def process_command(statement: str):
    statement = statement.lower().strip()
    if not statement or statement == "none":
        return

    chat.insert_user(statement)

    # Exit
    if any(phrase in statement for phrase in ["good bye", "okay bye", "turn off", "exit", "stop listening"]):
        speak(f"See you later, {USER_NAME}!")
        os._exit(0)

    # Thank You
    elif any(word in statement for word in ["thank", "thanks", "thank you", "appreciate it"]):
        speak(f"You're welcome, {USER_NAME}! Always happy to help.")

    # Wikipedia
    elif "wikipedia" in statement:
        speak("Searching Wikipedia...")
        query = statement.replace("wikipedia", "").strip()
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        except Exception:
            speak("Sorry, I couldn't find anything on Wikipedia.")

    # Websites
    elif "open youtube" in statement:
        webbrowser.open_new_tab("https://youtube.com")
        speak("YouTube is now open.")

    elif "open google" in statement:
        webbrowser.open_new_tab("https://google.com")
        speak("Google Chrome is open now.")

    elif "open gmail" in statement:
        webbrowser.open_new_tab("https://mail.google.com")
        speak("Google Mail is open now.")

    elif "open veeam" in statement:
        webbrowser.open_new_tab("https://veeam.com")
        speak("Veeam is open now.")

    elif "open the business" in statement:
        webbrowser.open_new_tab("https://topsocalproperties.com")
        speak("Top SoCal Properties is open now.")

    elif "open amazon" in statement:
        webbrowser.open_new_tab("https://amazon.com")
        speak("Amazon is open now.")

    # Minecraft
    elif "open minecraft" in statement:
        minecraft_path = r"C:\Program Files (x86)\Minecraft Launcher\MinecraftLauncher.exe"
        if os.path.exists(minecraft_path):
            os.startfile(minecraft_path)
            speak("Minecraft is now open.")
        else:
            try:
                os.system("start minecraft:")
                speak("Minecraft is now open.")
            except Exception:
                speak("I couldn't open Minecraft.")

    # Rainbow Parrot
    elif "parrot" in statement:
        rainbow_parrot()

    # Math Questions
    elif any(word in statement for word in ["calculate", "what is", "solve", "what's"]):
        query = statement
        for kw in ["calculate", "what is", "solve", "what's"]:
            query = query.replace(kw, "")
        query = query.strip()

        safe_chars = "0123456789+-*/(). "
        safe_query = "".join(c for c in query if c in safe_chars)

        if safe_query:
            try:
                result = eval(safe_query)
                speak(f"The answer is {result}, {USER_NAME}.")
                threading.Thread(target=show_math_popup, args=(safe_query, str(result))).start()
                return
            except Exception:
                pass

        # WolframAlpha fallback
        try:
            res = client.query(query)
            answer = next(res.results).text
            speak(f"The answer is {answer}, {USER_NAME}.")
            threading.Thread(target=show_math_popup, args=(query, answer)).start()
        except Exception:
            speak(f"Sorry, {USER_NAME}, I couldn't solve that.")

    # Unknown / AI Chat
    else:
        handle_small_talk(statement)

# === Microphone Listener ===
def listen_for_commands():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        speak(f"Edith is now listening, {USER_NAME}. Say 'Hey Edith' to wake me up.")

    while True:
        try:
            with mic as source:
                audio = r.listen(source, timeout=10, phrase_time_limit=5)
                wake_text = r.recognize_google(audio, language='en-in').lower()
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue
        except Exception as e:
            print("Error:", e)
            continue

        if "hey edith" in wake_text or "edith" in wake_text:
            speak(f"Yes, {USER_NAME}? I'm listening.")
            try:
                with mic as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    command_audio = r.listen(source, timeout=7, phrase_time_limit=10)
                    command = r.recognize_google(command_audio, language='en-in')
                    process_command(command)
            except sr.UnknownValueError:
                speak(f"Sorry, {USER_NAME}, I didn't catch that.")
            except sr.WaitTimeoutError:
                speak(f"I didn’t hear a command, {USER_NAME}.")
            except Exception as e:
                print("Error:", e)
                speak(f"Something went wrong, {USER_NAME}.")

# === Run Assistant ===
def main():
    speak("Loading Edith...")
    time.sleep(0.3)
    wishMe()
    listener_thread = threading.Thread(target=listen_for_commands)
    listener_thread.daemon = True
    listener_thread.start()
    chat.window.mainloop()

if __name__ == '__main__':
    main()
