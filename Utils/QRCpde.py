import pyqrcode
import png

from utils.utils import GetDownloadFolder

def CreateQRCode(fileName):
    try:
        downloadPath = GetDownloadFolder()
        url=pyqrcode.create(fileName)
        url.png(f"{downloadPath}\\{fileName}.png", scale=6)
        return True
    except Exception as e:
        print(f'Error al crear el QR Code: {e}')
        return False