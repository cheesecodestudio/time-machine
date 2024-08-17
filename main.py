from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils

from Utils.utils import ResizeImage, GenerateId, RelativePath
from Utils.textToSpeach import TextToSpeach
from Utils.QRCpde import CreateQRCode

# Main window
window = Tk()
WIDTH = window.winfo_screenwidth()
HEIGHT = window.winfo_screenheight()
window.attributes('-fullscreen', True)
window.title("Viaje con los antepasados")

# Background ====================================================#
imgBackground = ResizeImage(WIDTH, HEIGHT, ".\\resources\\imgs\\Background.png")
background = Label(image = imgBackground, text = "Background",border=0)
background.place(relx=0.5, rely=0.5, anchor= CENTER, bordermode="ignore")

# Video Control ==================================================#
# Commands
def play():
    print("play")

def pause():
    print("pause")

def repeat():
    print("repeat")

def close():
    print("close")

# Buttons
imgPlay = ResizeImage(50, 50, ".\\resources\\imgs\\buttons\\play.png")
btnPlay = Button(window, text="PLAY", image=imgPlay, height="50", width="50", command=play)
btnPlay.place(x = WIDTH/2, y = HEIGHT/4*3, anchor= CENTER)

imgPause = ResizeImage(50, 50, ".\\resources\\imgs\\buttons\\pause.png")
btnPause = Button(window, text="PAUSE", image=imgPause, height="50", width="50", command=pause)
btnPause.place(x = WIDTH/2, y = HEIGHT/4*3+55, anchor= CENTER)

imgRepeat = ResizeImage(50, 50, ".\\resources\\imgs\\buttons\\repeat.png")
btnRepeat = Button(window, text="REPEAT", image=imgRepeat, height="50", width="50", command=repeat)
btnRepeat.place(x = WIDTH/2-55, y = HEIGHT/4*3, anchor= CENTER)

imgClose = ResizeImage(50, 50, ".\\resources\\imgs\\buttons\\close.png")
btnClose = Button(window, text="CLOSE", image=imgClose, height="50", width="50", command=close)
btnClose.place(x = WIDTH/2+55, y = HEIGHT/4*3, anchor= CENTER)

# Camara ==================================================#
# Commands
# Funcion Visualizar
def visualizar():
    global window, frame
    # Leemos la videocaptura
    if cap is not None:
        ret, frame = cap.read()

        # Si es correcta
        if ret == True:
            # Rendimensionamos el video
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = imutils.resize(frame, width=100)

            # Convertimos el video
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(im)

            # Mostramos en el GUI
            camara.configure(image=img)
            camara.image = img
            camara.after(10, visualizar)
        else:
            cap.release()

def start():
    global cap
    # Elegimos la camara
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    visualizar()
    
def end():
    cap.release()

# Video
camara = Label(window)
camara.place(x = WIDTH/5*4, y = HEIGHT/4*3+10, anchor=CENTER)

# Frame
frame = Label(window, width=100, height=30)
frame.place(x = WIDTH/4*2, y = HEIGHT/4*3-100, anchor="s")

# Buttons
imgStart = ResizeImage(50, 50, ".\\resources\\imgs\\buttons\\start.png")
btnStart = Button(window, text="START", image=imgStart, height="50", width="50", command=start)
btnStart.place(x = 0, y = 0)

imgEnd = ResizeImage(50, 50, ".\\resources\\imgs\\buttons\\end.png")
btnEnd = Button(window, text="END", image=imgEnd, height="50", width="50", command=end)
btnEnd.place(x = 55, y = 0)

# Audio and Images ==================================================#

# Commands
def selectImages():
    print("Select images")

def generateInfo():
    nameFile = GenerateId()
    # Debe ser de extension .wav
    relativePath = RelativePath(f"output\\audios\\{nameFile}.wav")
    
    TextToSpeach(txtHistory.get(1.0, END), relativePath)
    CreateQRCode(str(nameFile))
    
    

# Generate QR Code
def generateQRCode():
    global QRCodeWindow, txtHistory
    QRCODE_WIDTH = 500
    QRCODE_HEIGHT = 700
    QRCodeWindow = Toplevel()
    QRCodeWindow.title("Create QR Code")
    QRCodeWindow.geometry(f"{QRCODE_WIDTH}x{QRCODE_HEIGHT}")  # Asignamos la dimension de la ventana

    imgSelectImgs = ResizeImage(50, 50, ".\\resources\\imgs\\buttons\\upload.png")
    btnSelectImgs = Button(QRCodeWindow, text="SELECTIMGS", image=imgSelectImgs, width="300", height="50", command=selectImages)
    btnSelectImgs.place(x = QRCODE_WIDTH/2, y = 40, anchor=CENTER)

    # Create an Entry widget
    txtHistory = Text(QRCodeWindow, width=300, height=200)
    txtHistory.pack(padx = 10, pady = 80)
    
    imgQRCode = ResizeImage(50, 50, ".\\resources\\imgs\\buttons\\upload.png")
    btnQRCode = Button(QRCodeWindow, text="QRCODE", image=imgQRCode, width="300", height="50", command=generateInfo)
    btnQRCode.place(x = QRCODE_WIDTH/2, y = QRCODE_HEIGHT-40, anchor=CENTER)

    QRCodeWindow.bind('<Escape>', lambda e: close_window(e))
    QRCodeWindow.mainloop()

# Buttons
imgGenerateQR = ResizeImage(50, 50, ".\\resources\\imgs\\buttons\\upload.png")
btnGenerateQR = Button(window, text="UPLOAD", image=imgGenerateQR, height="50", width="50", command=generateQRCode)
btnGenerateQR.place(x = WIDTH/5*4, y = HEIGHT/2, anchor=CENTER)

# Functionality/Template ==================================================#
# Commands
# Buttons

# Close Window ==================================================#
def close_window(event):
    window.destroy()

window.bind('<Escape>', lambda e: close_window(e))

#================================================================#
window.mainloop()