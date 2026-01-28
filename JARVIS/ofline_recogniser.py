import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
from queue import Queue

SAMPLE_RATE = 16000
BLOCK_SIZE = 8000  # Thoda bada block size better word recognition ke liye

model_path = r"C:\Users\Avik Maji\Desktop\vosk-model-en-in-0.5\vosk-model-en-in-0.5"
model = Model(model_path)

def offline_recogniser():
    """
    Generator function: continuously yields recognized text (words/phrases)
    instead of individual characters.
    """
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    rec.SetWords(True)
    q = Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status)
        if rec.AcceptWaveform(bytes(indata)):
            result = json.loads(rec.Result())
            text = result.get("text", "").strip()
            if text:
                q.put(text)

    try:
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            dtype='int16',
            channels=1,
            callback=callback
        ):
            while True:
                if not q.empty():
                    yield q.get()  # Continuous generator
    except KeyboardInterrupt:
        print("\n❌ Stopped")
        return

# Example usage:
if __name__ == "__main__":
    for recognized_text in offline_recogniser():
        print("✅ Recognized:", recognized_text)
