import pyautogui
import pyttsx3
from ofline_recogniser import offline_recogniser

#======================Talking=================#
def speak(text):
    # text = str(text)
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    engine.say(text)
    engine.runAndWait()

#==============INSTAGRAM SECTION==============#

def mute_video():
    loc = pyautogui.locateCenterOnScreen("mute.png", confidence=0.7, grayscale=True)
    if loc:
        pyautogui.click(loc)
        speak("Video muted")

def unmute_video():
    loc = pyautogui.locateCenterOnScreen("unmute.png", confidence=0.7, grayscale=True)
    if loc:
        pyautogui.click(loc)
        speak("Video unmuted")

def reelsscrolling(command):
    command = str(command).lower().strip()
    print("🎙 Command:", command)

    if "scroll down" in command:
        pyautogui.scroll(-150)
        speak("Scrolling down")

    elif "scroll up" in command:
        pyautogui.scroll(150)
        speak("Scrolling up")

    elif "mute" in command:
        mute_video()

    elif "unmukt" in command or "unmute" in command:
        unmute_video()

    elif "refresh" in command:
        pyautogui.hotkey('ctrl', 'r')
        speak("Page refreshed")

    elif "stop instagram" in command:
        speak("Stopping Instagram control")
        return "STOP"

#==============ACTIVE MODE==============#

def jarvis_active_mode():
    speak("Instagram mode activated")

    for command in offline_recogniser():
        if not command:
            continue

        if "stop instagram" in command:
            speak("Instagram control stopped")
            break

        result = reelsscrolling(command)
        if result == "STOP":
            break

#==============WAKE WORD MODE==============#

def wake_word_listener():
    speak("Jarvis initialized. Say Jarvis")

    for text in offline_recogniser():
        if not text:
            continue

        print("✅ Recognized: ", text)

        if "jarvis" in str(text).lower():
            speak("Yes")
            jarvis_active_mode()

#==============MAIN==============#

if __name__ == "__main__":
    wake_word_listener()
