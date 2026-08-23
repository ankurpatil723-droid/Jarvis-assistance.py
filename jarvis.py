"""
JARVIS - A Simple Beginner-Friendly Voice Assistant
-----------------------------------------------------
Say "Jarvis" to wake it up, then speak a command.

Supported commands:
    - "open youtube"
    - "open google"
    - "open vs code"
    - "open chrome"
    - "open calculator"
    - "open notepad"
    - "search <something>"
    - "what time is it"
    - "stop" / "exit" / "bye"
"""

import webbrowser
import subprocess
import datetime
import speech_recognition as sr
import pyttsx3

# ---------------------------------------------------------
# SETUP: Text-to-Speech engine
# ---------------------------------------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 170)  # speaking speed


def speak(text):
    """Make JARVIS speak the given text and also print it."""
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()


# ---------------------------------------------------------
# SETUP: Speech Recognition
# ---------------------------------------------------------
recognizer = sr.Recognizer()


def listen():
    """
    Listen through the microphone and return recognized text (lowercase).
    Returns an empty string if nothing understandable was heard.
    """
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)

        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()

    except sr.WaitTimeoutError:
        # No speech detected in time - just try again
        return ""
    except sr.UnknownValueError:
        # Speech was not understandable
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is unavailable right now.")
        return ""
    except OSError:
        # Raised when no microphone is found
        speak("I can't access the microphone. Please check your microphone connection.")
        return ""


# ---------------------------------------------------------
# APP LAUNCHER HELPER
# ---------------------------------------------------------
def open_application(path_or_name, friendly_name):
    """
    Try to open a Windows application using subprocess.
    Shows a friendly error if it's not found.
    """
    try:
        subprocess.Popen(path_or_name)
        speak(f"Opening {friendly_name}")
    except FileNotFoundError:
        speak(f"I couldn't find {friendly_name} on this computer.")
    except Exception as e:
        speak(f"Something went wrong while opening {friendly_name}.")
        print(f"Error: {e}")


# ---------------------------------------------------------
# COMMAND HANDLER
# ---------------------------------------------------------
def handle_command(command):
    """
    Look at the recognized command text and perform the matching action.
    Returns False if JARVIS should stop, True otherwise.
    """

    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open vs code" in command or "open visual studio code" in command:
        # "code" is the VS Code command-line launcher (must be in PATH)
        open_application("code", "VS Code")

    elif "open chrome" in command:
        # Common Chrome install path on Windows
        open_application(
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "Chrome"
        )

    elif "open calculator" in command:
        open_application("calc.exe", "Calculator")

    elif "open notepad" in command:
        open_application("notepad.exe", "Notepad")

    elif "search" in command:
        # Extract the search query after the word "search"
        query = command.split("search", 1)[1].strip()
        if query:
            speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What would you like me to search for?")

    elif "what time is it" in command or "current time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "stop" in command or "exit" in command or "bye" in command:
        speak("Goodbye!")
        return False

    else:
        speak("Sorry, I didn't understand that command.")

    return True


# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
def main():
    speak("JARVIS is ready. Say 'Jarvis' to wake me up.")

    running = True
    while running:
        text = listen()

        if not text:
            continue  # nothing heard, just keep listening

        # Wake word check
        if "jarvis" in text:
            speak("Yes?")
            command = listen()

            if command:
                running = handle_command(command)
            else:
                speak("I didn't catch that. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Shutting down. Goodbye!")
