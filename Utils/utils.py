from PIL import Image, ImageTk
import uuid
import os
from pathlib import Path

def ResizeImage(width, height, imagePath):
    # Open an image file
    image = Image.open(imagePath)
    # Resize the image
    resized_image = image.resize((width, height))
    # Convert the resized image to a PhotoImage object
    return ImageTk.PhotoImage(resized_image)

def GenerateId():
    return uuid.uuid4()

def RelativePath(path, start=""):
    if start != "":
        return os.path.relpath(path, start)
    return os.path.relpath(path)

def GetDownloadFolder():
    home = Path.home()
    return os.path.join(str(home), "Downloads")

def SaveFiles(imagesPaths, destinationFolder):
    if len(imagesPaths) <= 0:
        return False
    # Asegurarse de que la carpeta de destino existe
    if not os.path.exists(destinationFolder):
        os.makedirs(destinationFolder)

    for imagePath in imagesPaths:
        if os.path.isfile(imagePath):
            try:
                # Abrir la imagen usando Pillow
                img = Image.open(imagePath)
                
                # Obtener el nombre de archivo de la imagen
                imageName = os.path.basename(imagePath)
                
                # Definir la ruta completa del archivo en la carpeta de destino
                destinationPath = os.path.join(destinationFolder, imageName)
                
                # Guardar la imagen en la carpeta de destino
                img.save(destinationPath)
            except Exception as e:
                print(f'Error al copiar {imagePath}: {e}')
                return False
        else:
            print(f'{imagePath} no es un archivo válido.')
            return False
    return True