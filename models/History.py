from audioplayer import AudioPlayer
import os

class History:
    def __init__(self):
        self.fileName = ""
        self.player = None
        self.state = ""
        self.image_paths = []
        self.delay = 5000
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

    def audio_controller(self):
        if self.is_speaking():
            # Stop the audio
            if keyboard.is_pressed('6'):
                self.player.stop()
                self.state = ""
            
            # Repeat the audio
            if keyboard.is_pressed('4'):
                self.player.play()
                self.state = "playing"
            
            # Pause the audio
            if keyboard.is_pressed('5'):
                self.player.pause()
                self.state = "pause"

            # Resume the audio
            if keyboard.is_pressed('2'):
                self.player.resume()
                self.state = "playing"