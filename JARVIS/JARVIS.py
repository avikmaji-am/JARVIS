import os
import webbrowser
import pyttsx3
import requests
import subprocess
import time
import datetime
import pyautogui
import pygetwindow as pgw
import psutil

# module made in this PC
import music
import aireply as ai
import special_automation_for_instagram as safi
from ofline_recogniser import offline_recogniser


# ============================
# Voice
# ============================
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()


# ============================
# Known Apps
# ============================
KNOWN_APPS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "whatsapp": "whatsapp",
    "vs code": "code",
    "explorer": "explorer",
    "photos": "photos"
}


# ============================
# NORMALIZER (ONLY THIS)
# ============================
def normalize_app_name(app_name, for_close=False):
    app_name = str(app_name).lower().strip()

    whatsapp_aliases = [
        "whatsapp", "watsa", "watson", "what", "words", "work", "word",
        "toward", "towards", "ward said" , "warship"
    ]

    brave_aliases = ["brave", "grave", "breve", "brove", "brav"]
    chrome_aliases = ["chrome", "chrom", "crome", "krom"]
    vscode_aliases = ["vs code", "vscode", "visual studio", "editor"]
    explorer_aliases = ["file explorer", "explorer", "files", "folders"]

    for a in whatsapp_aliases:
        if a in app_name:
            return "whatsapp.exe" if for_close else "whatsapp"

    for a in brave_aliases:
        if a in app_name:
            return "brave.exe" if for_close else "brave"

    for a in chrome_aliases:
        if a in app_name:
            return "chrome.exe" if for_close else "chrome"

    for a in vscode_aliases:
        if a in app_name:
            return "code.exe" if for_close else "vs code"

    for a in explorer_aliases:
        if a in app_name:
            return "explorer.exe" if for_close else "explorer"

    return f"{app_name}.exe" if for_close else app_name

CLOSE_TRIGGERS = ["close", "blues" ,"clues"]
# ============================
# Open App
# ============================
def open_app(app_name):
    app_name = normalize_app_name(app_name)
    
    pyautogui.press('win')
    time.sleep(1.5)

    pyautogui.write(f'{app_name}')
    time.sleep(0.5)
    pyautogui.press('enter')



# ============================
# Minimize App
# ============================
def minimize_app(app_name):
    app_name = normalize_app_name(app_name)

    windows = pgw.getWindowsWithTitle(app_name)
    if windows:
        windows[0].minimize()
        speak(f"{app_name} minimized")
        return True

    speak(f"App {app_name} not found")
    return False



# ============================
# Close App
# ============================
def close_application(command):
    command = str(command).lower().strip()

    # ------------------------
    # 1️ Remove all CLOSE_TRIGGERS from command
    # ------------------------
    for trig in CLOSE_TRIGGERS:
        if command.startswith(trig + " "):
            command = command.replace(trig, "", 1).strip()
            break

    if not command:
        speak("No application specified to close")
        return

    # ------------------------
    # 2️ Normalize app name
    # ------------------------
    app_name = normalize_app_name(command, for_close=True)
    print(f"Normalized app for closing: {app_name}")

    # ------------------------
    # 3️ Close logic
    # ------------------------
    if app_name.lower() == "whatsapp.exe":
        # WhatsApp is special because it's a UWP app (ApplicationFrameHost.exe)
        windows = pgw.getWindowsWithTitle("WhatsApp")
        if windows:
            for win in windows:
                win.close()
            speak("WhatsApp closed")
            print("WhatsApp closed")
        else:
            speak("WhatsApp is not running")
            print("WhatsApp is not running")
    else:
        # Normal .exe apps
        try:
            # Check if process exists
            task_check = os.popen(f'tasklist /fi "imagename eq {app_name}"').read()
            if app_name.lower() in task_check.lower():
                os.system(f'taskkill /f /im "{app_name}" >nul 2>&1')
                speak(f"{app_name.replace('.exe','')} closed")
                print(f"{app_name} closed")
            else:
                speak(f"{app_name.replace('.exe','')} is not running")
                print(f"{app_name} is not running")
        except Exception as e:
            speak(f"Failed to close {app_name.replace('.exe','')}")
            print(f"Error closing {app_name}: {e}")


# ============================
#                            #
# ============================


# ============================
#          switchTab         #
# ============================


def switch_tab() :
    pyautogui.hotkey("ctrl", "tab")
    print("Tab switched")
    speak("Tab switched")
# ============================
#                            #
# ============================



# ============================
#          Close Tab         #
# ============================


def close_browser_tab() :
    pyautogui.hotkey("ctrl", "w")
    print("Tab closed")
    speak("Tab Closed")
# ============================
#                            #
# ============================








# ============================
# Process Command
# ============================
def ProcessCommand(command):
    command = str(command).lower().strip()
    
    
    if command.startswith("start "):
        open_app(command.replace("start ", "").strip())

    elif command.startswith("open "):
        site = command.replace("open ", "").strip()
        if site:
            speak(f"Opening {site}")
            webbrowser.open(f"https://{site}.com")

    elif command.startswith("play "):
        song = command.replace("play ", "").strip()
        link = music.music.get(song)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Song not found")
            
            
    elif "closetab" == str(command).lower().strip().replace(" ","") :
        close_browser_tab("Brave")
    elif "switchtab" == str(command).lower().strip().replace(" ","") :
        switch_tab("Brave", "next")
            
    elif "thetime" in str(command).lower().strip().replace(" ",""):
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")
        print(f"{strTime}")
    elif "thedate" in str(command).lower().strip().replace(" ",""):
        strDate = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"The date is {strDate}")
        print(f"{strDate}")
    
    
    elif "news" in command:
        try:
            req = requests.get(
                "https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=( ADD Your API Key Here)"
            )
            for a in req.json().get("articles", [])[:5]:
                speak(a["title"])
        except:
            speak("Unable to fetch news")

    elif command.startswith(("minimise ", "minimize ")):
        minimize_app(command.replace("minimise ", "").replace("minimize ", "").strip())

    elif "instagramcontrol" in command.replace(" " , "") or "instacontrol" in command.replace(" " , ""):
        safi.jarvis_active_mode()
        
    elif any(command.startswith(word + " ") for word in CLOSE_TRIGGERS):
        # Close the application
        close_application(command)



# ============================
# Main Loop
# ============================
if __name__ == "__main__":
    speak("Initializing Jarvis")
    

    try:
        while True:
            
            for word in offline_recogniser():
                print("Detected:", word)
                if any(k in str(word).lower() for k in ["jarvis", "jar", "service" , "gervais" , "jerseys" , "jervis"]):
                    speak("I am listening")
                    print("🟢 Jarvis Active")

                    for cmd in offline_recogniser():
                        print("Command:", cmd)
                        ProcessCommand(cmd)
                        break
        
    except KeyboardInterrupt:
        speak("Jarvis shutting down")
