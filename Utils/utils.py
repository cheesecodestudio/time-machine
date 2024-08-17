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
