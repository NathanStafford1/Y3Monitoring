import speech_recognition

# Obtain audio from the mic
recognizer = speech_recognition.Recognizer()
with speech_recognition.Microphone() as source:
    print("Say something")
    audio = recognizer.listen(source)

# Use Google Speech Recognition to work out the audio
print("You said")
print(recognizer.recognize_google(audio))
