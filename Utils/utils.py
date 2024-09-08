from PIL import Image, ImageTk
import uuid
import os
from pathlib import Path
import shutil

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

def SaveImageFiles(imagesPaths, destinationFolder):
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

def SaveAudioFile(audioPath, destinationFolder):
    # Asegurarse de que la carpeta de destino existe
    if not os.path.exists(destinationFolder):
        os.makedirs(destinationFolder)
    
    if os.path.isfile(audioPath):
        try:
            # Obtener el nombre de archivo de la imagen
            audioName = os.path.basename(audioPath)

            if not audioName.find(".wav"):
                raise Exception("El formato del archivo no es válido.")
            
            # Definir la ruta completa del archivo en la carpeta de destino
            destinationPath = os.path.join(destinationFolder, audioName)
            
            shutil.copy(audioPath, destinationPath)
            return True
        except Exception as e:
            print(e)
            return False
    else:
        print(f'{audioPath} no es un archivo válido.')
        return False