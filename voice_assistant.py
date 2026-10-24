import tkinter as tk
import pyttsx3 
import speech_recognition as sr
import webbrowser
from datetime import datetime
import threading

# Setup
engine = pyttsx3.init()
engine.setProperty("rate", 160)
recognizer = sr.Recognizer()

# Colors
BG = "#F8F5F7"
WHITE = "#FFFFFF"
PURPLE = "#7A629A"
PINK = "#D96C94"
DARK = "#403842"
GREY = "#777078"
GREEN = "#4C956C"
SOFT_PINK = "#C18AA0"

# Window
root = tk.Tk()
root.title("Agent Nova - Voice Assistant")
root.geometry("900x600")
root.configure(bg=BG)


# ---------- Functions ----------

def speak(text):
    engine.say(text)
    engine.runAndWait()


def add_message(name, text):
    chat.config(state="normal")
    chat.insert(tk.END, name + "\n", name)
    chat.insert(tk.END, text + "\n\n", "text")
    chat.config(state="disabled")
    chat.see(tk.END)


def respond(text):
    add_message("Agent Nova", text)


def command(text):
    text = text.lower().strip()

    if "hello" in text or "hi" in text:
        respond("Hello! How can I help you?")

    elif "time" in text:
        respond("The current time is " +
                datetime.now().strftime("%I:%M %p"))

    elif "date" in text or "today" in text:
        respond("Today's date is " +
                datetime.now().strftime("%d %B %Y"))

    elif "open google" in text:
        webbrowser.open("https://google.com")
        respond("Opening Google.")

    elif "open youtube" in text:
        webbrowser.open("https://youtube.com")
        respond("Opening YouTube.")

    elif text.startswith("search"):
        search = text.replace("search", "", 1).strip()

        if search:
            webbrowser.open(
                "https://www.google.com/search?q=" +
                search.replace(" ", "+")
            )
            respond("Searching for " + search)
        else:
            respond("Please tell me what you want to search.")

    elif "bye" in text or "exit" in text:
        respond("Goodbye!")
        root.after(1200, root.destroy)

    else:
        respond("I heard you say: " + text)


def send():
    text = entry.get().strip()

    if text:
        add_message("You", text)
        entry.delete(0, tk.END)
        command(text)


def text_to_speech():
    text = entry.get().strip()

    if text:
        add_message("You", text)
        entry.delete(0, tk.END)

        threading.Thread(
            target=speak,
            args=(text,),
            daemon=True
        ).start()


def listen():

    def voice():
        try:
            status.config(text="● Listening...", fg=PINK)

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(
                    source, duration=0.5
                )
                audio = recognizer.listen(
                    source, timeout=5, phrase_time_limit=7
                )

            text = recognizer.recognize_google(audio)

            root.after(0, lambda: speech_result(text))

        except:
            root.after(
                0,
                lambda: status.config(
                    text="● Ready", fg=GREEN
                )
            )

    threading.Thread(target=voice, daemon=True).start()


def speech_result(text):
    status.config(text="● Ready", fg=GREEN)
    entry.delete(0, tk.END)
    entry.insert(0, text)


def clear():
    chat.config(state="normal")
    chat.delete("1.0", tk.END)
    chat.config(state="disabled")


# ---------- Header ----------

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=40, pady=(25, 15))

tk.Label(
    header,
    text="Agent Nova",
    font=("Segoe UI", 26, "bold"),
    bg=BG,
    fg=PURPLE
).pack(side="left")

tk.Label(
    header,
    text="Python Voice Assistant",
    font=("Segoe UI", 11),
    bg=BG,
    fg=GREY
).pack(side="left", padx=15)

status = tk.Label(
    header,
    text="● Ready",
    font=("Segoe UI", 10, "bold"),
    bg=BG,
    fg=GREEN
)
status.pack(side="right")


# ---------- Chat ----------

chat = tk.Text(
    root,
    height=16,
    bg=WHITE,
    fg=DARK,
    font=("Segoe UI", 11),
    relief="solid",
    bd=1,
    wrap="word",
    padx=20,
    pady=15
)
chat.pack(fill="both", expand=True, padx=40, pady=10)

chat.tag_config(
    "Agent Nova",
    foreground=PURPLE,
    font=("Segoe UI", 10, "bold")
)

chat.tag_config(
    "You",
    foreground=PINK,
    font=("Segoe UI", 10, "bold")
)

chat.tag_config(
    "text",
    foreground=DARK
)

chat.config(state="disabled")


# ---------- Input ----------

frame = tk.Frame(root, bg=BG)
frame.pack(fill="x", padx=40, pady=(5, 20))

entry = tk.Entry(
    frame,
    font=("Segoe UI", 12),
    bg=WHITE,
    fg=DARK,
    relief="solid",
    bd=1
)
entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=12,
    padx=(0, 8)
)


def make_button(text, command, color):
    return tk.Button(
        frame,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        activebackground=color,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=14,
        pady=10
    )


make_button("Send", send, PURPLE).pack(side="left", padx=4)

make_button(
    "🔊 Text to Speech",
    text_to_speech,
    PINK
).pack(side="left", padx=4)

make_button(
    "🎤 Speech to Text",
    listen,
    SOFT_PINK
).pack(side="left", padx=4)

make_button(
    "Clear",
    clear,
    "#958C96"
).pack(side="left", padx=4)


# Welcome
root.after(
    500,
    lambda: add_message(
        "Agent Nova",
        "Hello! Type a command or use Text to Speech / Speech to Text."
    )
)

root.mainloop()
