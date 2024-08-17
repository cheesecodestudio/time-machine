from audioplayer import AudioPlayer
import keyboard

# Playback stops when the object is destroyed (GC'ed), so save a reference to the object for non-blocking playback.
# AudioPlayer("./audios/pato_de_goma.wav").play(block=True)

key = keyboard.read_key()  # Espera a que se presione una tecla
print(f"Tecla presionada: {key}")