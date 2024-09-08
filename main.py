from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import imutils

from utils.utils import ResizeImage
from models.History import History
from components.GenerateQR import generateQRCode

# Main window
history = History()
window = Tk()
WIDTH = window.winfo_screenwidth()
HEIGHT = window.winfo_screenheight()
BUTTON_SIZE = 100
isStart = False
window.attributes('-fullscreen', True)
window.title("Máquina del Tiempo")

# Background ====================================================#
imgBackground = ResizeImage(WIDTH, HEIGHT, ".\\assets\\imgs\\Background.png")
background = Label(image = imgBackground, text = "Background",border=0)
background.place(relx=0.5, rely=0.5, anchor= CENTER, bordermode="ignore")

# Video Control ==================================================#
# Commands
def play():
    if history.state == "playing":
        history.pause()
        btnPlay.configure(image=imgPlay)
    elif history.state == "pause":
        history.resume()
        btnPlay.configure(image=imgPause)

def repeat():
    history.repeat()

def close():
    history.stop()

# Buttons
imgPlay = ResizeImage(BUTTON_SIZE, BUTTON_SIZE, ".\\assets\\imgs\\buttons\\play.png")
imgPause = ResizeImage(BUTTON_SIZE, BUTTON_SIZE, ".\\assets\\imgs\\buttons\\pause.png")
btnPlay = Button(window, text="PLAY", image=imgPause, height=f"{BUTTON_SIZE}", width=f"{BUTTON_SIZE}", command=play)
btnPlay.place(x = WIDTH/2, y = HEIGHT/4*3, anchor= CENTER)

imgRepeat = ResizeImage(BUTTON_SIZE, BUTTON_SIZE, ".\\assets\\imgs\\buttons\\repeat.png")
btnRepeat = Button(window, text="REPEAT", image=imgRepeat, height=f"{BUTTON_SIZE}", width=f"{BUTTON_SIZE}", command=repeat)
btnRepeat.place(x = WIDTH/2-(BUTTON_SIZE+5), y = HEIGHT/4*3, anchor= CENTER)

imgClose = ResizeImage(BUTTON_SIZE, BUTTON_SIZE, ".\\assets\\imgs\\buttons\\close.png")
btnClose = Button(window, text="CLOSE", image=imgClose, height=f"{BUTTON_SIZE}", width=f"{BUTTON_SIZE}", command=close)
btnClose.place(x = WIDTH/2+(BUTTON_SIZE+5), y = HEIGHT/4*3, anchor= CENTER)

# Camara ==================================================#
# Commands
def camara_view():
    global window, frame, qr_detector, frame_view
    # Leemos la videocaptura
    if cap is not None:
        ret, frame = cap.read()

        # Si es correcta
        if ret == True:
            history.audio_controller()
            # Detect QR Code
            data, bbox, _ = qr_detector.detectAndDecode(frame)
            if data:
                if history.change_person(data):
                    history.create(data)
                    
                    # Cargar la primera imagen
                    history_image = cv2.imread(history.image_paths[history.index_images])
                    history_image = imutils.resize(history_image, width=500) # Rendimensionamos el video
                    photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(history_image, cv2.COLOR_BGR2RGB)))

                    # Mostramos en el GUI
                    frame_view.configure(image=photo)
                    frame_view.image = photo

                    # Iniciar el ciclo de cambio de imágenes
                    update_image()

            # Rendimensionamos el video
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = imutils.resize(frame, width=100)

            # Convertimos el video
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(im)

            # Mostramos en el GUI
            camara.configure(image=img)
            camara.image = img
            camara.after(10, camara_view)
        else:
            cap.release()

def update_image():
    global history, frame_view
    # Incrementar el índice para la siguiente imagen
    history.index_images = (history.index_images + 1) % len(history.image_paths)
    
    # Cargar la primera imagen
    history_image = cv2.imread(history.image_paths[history.index_images])
    history_image = imutils.resize(history_image, width=400) # Rendimensionamos el video
    photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(history_image, cv2.COLOR_BGR2RGB)))

    # Mostramos en el GUI
    frame_view.configure(image=photo, width=500)
    frame_view.image = photo
    
    # Programar la siguiente actualización
    frame_view.after(history.delay, update_image)

def start():
    global cap, qr_detector, isStart
    if not isStart:
        cap = cv2.VideoCapture(camara_selected.get(), cv2.CAP_DSHOW)
        qr_detector = cv2.QRCodeDetector()
        camara_view()
        isStart = True
        btnStart.configure(image=imgEnd)
    else:
        cap.release()
        isStart = False
        btnStart.configure(image=imgStart)

# Video
camara = Label(window)
camara.place(x = WIDTH/5*4, y = HEIGHT/4*3+10, anchor=CENTER)

# Frame
frame_view = Label(window)
frame_view.place(x = WIDTH/4*2, y = HEIGHT/4*3-100, anchor="s")

# Buttons
imgStart = ResizeImage(BUTTON_SIZE, BUTTON_SIZE, ".\\assets\\imgs\\buttons\\start.png")
imgEnd = ResizeImage(BUTTON_SIZE, BUTTON_SIZE, ".\\assets\\imgs\\buttons\\end.png")
btnStart = Button(window, text="START", image=imgStart, height=f"{BUTTON_SIZE}", width=f"{BUTTON_SIZE}", command=start)
btnStart.place(x = 0, y = 0)

# Dropdown with video captures# datatype of menu text 
def get_video_inputs():
    """Detecta las cámaras de video conectadas y devuelve una lista con sus índices."""
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

camara_selected = IntVar() 
video_inputs = get_video_inputs()

# initial menu text 
camara_selected.set(video_inputs[0])

# Create Dropdown menu 
dropdown = ttk.OptionMenu(
    window, 
    camara_selected, 
    *video_inputs
)
dropdown.place(
    x=BUTTON_SIZE+10,
    y=0,
    width=BUTTON_SIZE,
    height=BUTTON_SIZE
)

# Audio and Images ==================================================#

# Buttons
imgGenerateQR = ResizeImage(BUTTON_SIZE, BUTTON_SIZE, ".\\assets\\imgs\\buttons\\generate_qr.png")
btnGenerateQR = Button(window, text="UPLOAD", image=imgGenerateQR, height=f"{BUTTON_SIZE}", width=f"{BUTTON_SIZE}", command=lambda: generateQRCode(window))
btnGenerateQR.place(x = WIDTH/5*4, y = HEIGHT/2, anchor=CENTER)

# Functionality/Template ==================================================#
# Commands
# Buttons

#================================================================#
window.bind('<Escape>', lambda e: window.destroy())
window.mainloop()