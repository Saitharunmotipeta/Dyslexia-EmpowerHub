import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 80)  # speed
engine.say("Hello Dyslexia Empower Hub")
engine.runAndWait()
engine.stop()