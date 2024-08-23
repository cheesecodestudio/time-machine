from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showwarning
from PIL import Image, ImageTk
import cv2
import imutils

from utils.utils import ResizeImage, GenerateId, RelativePath, SaveFiles
from utils.textToSpeach import TextToSpeach
from utils.QRCpde import CreateQRCode
from models.History import History

# Main window
history = History()
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
def camara_view():
    global window, frame, qr_detector, frame_view
    # Leemos la videocaptura
    if cap is not None:
        ret, frame = cap.read()

        # Si es correcta
        if ret == True:
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
    global cap, qr_detector
    # Elegimos la camara
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    qr_detector = cv2.QRCodeDetector()
    camara_view()

    
def end():
    cap.release()

# Video
camara = Label(window)
camara.place(x = WIDTH/5*4, y = HEIGHT/4*3+10, anchor=CENTER)

# Frame
frame_view = Label(window)
frame_view.place(x = WIDTH/4*2, y = HEIGHT/4*3-100, anchor="s")

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
    global imagesPaths
    filetypes = (
        ('PNG', '*.png'),
        ('JPG', '*.jpg'),
        ('JPEG', '*.jpeg')
    )

    imagesPaths = fd.askopenfilenames(
        title='Select images',
        initialdir='/',
        filetypes=filetypes)

def generateInfo():
    nameFile = GenerateId()
    # Debe ser de extension .wav
    relativePath = RelativePath(f"output\\audios\\{nameFile}.wav")
    
    if not SaveFiles(imagesPaths, RelativePath(f"output\\packImgs\\{nameFile}\\")):
        showwarning("Seleccionar imagenes", "Falta seleccionar imagenes para completar este proceso.")
        return
        
    if not TextToSpeach(txtHistory.get(1.0, END), relativePath):
        showwarning("Ingresar texto", "Falta ingresar un texto para completar este proceso.")
        return

    CreateQRCode(str(nameFile))
    showinfo("Información", "En la carpeta Descargas se creó el QR Code para que lo puedas utilizar.")

def generateQRCode():
    global QRCodeWindow, txtHistory, imagesPaths
    QRCODE_WIDTH = 500
    QRCODE_HEIGHT = 700
    QRCodeWindow = Toplevel()
    QRCodeWindow.title("Create QR Code")
    QRCodeWindow.geometry(f"{QRCODE_WIDTH}x{QRCODE_HEIGHT}")  # Asignamos la dimension de la ventana
    QRCodeWindow.transient(window)
    # Mantener el foco en la ventana toplevel
    QRCodeWindow.focus()
    # Evitar que la ventana toplevel se mueva detrás de la ventana principal
    QRCodeWindow.grab_set()
    
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