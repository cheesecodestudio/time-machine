import cv2
import threading
from audioplayer import AudioPlayer
import keyboard

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
