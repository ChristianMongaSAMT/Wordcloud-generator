from argparse import FileType
import filetype
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

path = './pictures/stellina.jpg'

def getPath():
    return path
def setPath(newPath):
    global path
    path = newPath

class ImageSelector(BoxLayout):
    txt = StringProperty()
    
    def __init__(self, row, **kwargs):
        super(ImageSelector, self).__init__(**kwargs)
        
        self.txt = row

    def updateImage(self, wcApp, tolerance, font,wordsOrderByEmphasis):
        self.wcApp = wcApp
        self.setPath()
        self.createBorderImage(tolerance, font, wordsOrderByEmphasis)

        tolPer = int((self.ids.tolerance_slider.value / 2000) * 100)
        tolValue = f'Tolerance: {str(tolPer)}%'
        self.ids.tolerance_label.text = tolValue

    def setPasfsdfth(self):
        # Controlla se è una path valida, se la path è un file e se è un'immagine
        
        if(not (os.path.exists(path) and os.path.isfile(path) and FileType.is_image(path))):
            self.imagepath = './pictures/default.png'
        else:
            self.imagepath = path

    def visualizer(self):
        # Memorizza la nuova path
        self.getPathFromTextInput()
        if((os.path.exists(getPath()) and os.path.isfile(getPath()) and filetype.is_image(getPath()))):
            # Se la path esiste la usa per l'immagine
            #imageSource = self.path
            print('valid path')
        else:
            # Se la path non esiste carica l'immagine di default
            newPath = './pictures/default.png'
            setPath(newPath)

    def getPathFromTextInput(self):
        # Prende la path per l'immagine dal text input
        path = self.ids.path.text
        path = path.strip()
        path = path.replace('"','')
        setPath(path)