import pyttsx3

def TextToSpeach(text, filePath):
    print(filePath)
    print(text)

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    # Set properties to match the chat voice as closely as possible
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    # Set the voice to a more conversational and natural sounding voice, if available
    voices = engine.getProperty('voices')
    spanish_voice = None
    for voice in voices:
        if 'spanish' in voice.name.lower():
            spanish_voice = voice.id
            break

    if spanish_voice:
        engine.setProperty('voice', spanish_voice)

    # Save the speech to a file
    engine.save_to_file(text, filePath)

    # Run and wait for the speech to be saved
    engine.runAndWait()