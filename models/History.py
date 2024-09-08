from audioplayer import AudioPlayer
import os
import keyboard

class History:
    def __init__(self):
        self.fileName = ""
        self.player = None
        self.state = ""
        self.image_paths = []
        self.delay = 10000
        self.index_images = 0

    def create(self, file_name):
        self.file_name = file_name
        path = f".\\output\\audios\\{file_name}.wav"
        self.player = AudioPlayer(path)
        self.player.play(loop=False)
        self.state = "playing"
        image_folder = f".\\output\\packImgs\\{file_name}"
        self.image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]


    def change_person(self, new_file_name):
        return self.player is None or self.file_name != new_file_name

    def is_speaking(self):
        return self.state != ""

    def repeat(self):
        if self.is_speaking():
            self.player.play()
            self.state = "playing"
    
    def resume(self):
        if self.is_speaking():
            self.player.resume()
            self.state = "playing"
    
    def pause(self):
        if self.is_speaking():
            self.player.pause()
            self.state = "pause"
    
    def stop(self):
        if self.is_speaking():
            self.player.stop()
            self.state = ""
            self.file_name = ""

    def audio_controller(self):
            # Stop the audio
        if keyboard.is_pressed('6'):
            self.stop()
        # Repeat the audio
        if keyboard.is_pressed('4'):
            self.repeat()
        # Pause the audio
        if keyboard.is_pressed('5'):
            self.pause()
        # Resume the audio
        if keyboard.is_pressed('2'):
            self.resume()
