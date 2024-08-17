import cv2
import threading
from audioplayer import AudioPlayer
import keyboard

class History:
    def __init__(self):
        self.path = ""
        self.player = None
        self.state = "" 

    def create(self, file_path):
        self.path = file_path
        self.player = AudioPlayer(self.path)
        self.player.play(loop=False)
        self.state = "playing"

    def change_person(self, new_path):
        return self.player is None or self.path != new_path

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

# 
def main():
    global history
    history = History()
    cap = cv2.VideoCapture(0)
    qr_detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect QR Code
        data, bbox, _ = qr_detector.detectAndDecode(frame)
        if data:
            if history.change_person(data):
                history.create("./audios/pato_de_goma.wav")

        #Show the window
        cv2.imshow("QR Code Scanner", frame)

        
        if cv2.waitKey(1):
            # Quite the app
            if keyboard.is_pressed('q'):
                break

            history.audio_controller()
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
