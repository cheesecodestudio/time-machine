import pyqrcode
import png

from Utils.utils import GetDownloadFolder

def CreateQRCode(fileName):
    downloadPath = GetDownloadFolder()
    url=pyqrcode.create(fileName)
    url.png(f"{downloadPath}\\{fileName}.png", scale=6)