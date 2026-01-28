import pyttsx3
from openai import OpenAI

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()

def aiprocess(command):
    client = OpenAI(api_key="Add Your API Key Here")

    stream = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Assistant."
            },
            {
                "role": "user",
                "content": command
            }
        ],
        stream=True,
    )

    # ✅ MUST be defined BEFORE the loop
    full_response = ""

    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
            full_response += event.delta

    print()  # new line after streaming
    return full_response

def aitalk(a):
    output = aiprocess(a)
    speak(output)










