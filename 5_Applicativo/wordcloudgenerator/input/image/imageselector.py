from argparse import FileType
import filetype
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class ImageSelector(BoxLayout):
    txt = StringProperty()

    path = './pictures/default.png'
    
    def __init__(self, row, **kwargs):
        super(ImageSelector, self).__init__(**kwargs)
        self.txt = row

    def updateImage(self, path, wcApp, tolerance, font,wordsOrderByEmphasis):
        self.wcApp = wcApp
        self.setPath(path)
        self.createBorderImage(tolerance, font, wordsOrderByEmphasis)

        tolPer = int((self.ids.tolerance_slider.value / 2000) * 100)
        tolValue = f'Tolerance: {str(tolPer)}%'
        self.ids.tolerance_label.text = tolValue

    def setPath(self, path):
        # Controlla se è una path valida, se la path è un file e se è un'immagine
        if(not (os.path.exists(path) and os.path.isfile(path) and FileType.is_image(path))):
            self.imagepath = './pictures/default.png'
        else:
            self.imagepath = path

    
    def visualizer(self):
        # Memorizza la nuova path
        self.getPathFromTextInput()

        if((os.path.exists(self.path) and os.path.isfile(self.path) and filetype.is_image(self.path))):
            # Se la path esiste la usa per l'immagine
            #imageSource = self.path
            print(self.path)
        else:
            # Se la path non esiste carica l'immagine di default
            self.path = './pictures/default.png'

    def getPathFromTextInput(self):
        # Prende la path per l'immagine dal text input
        self.path = self.ids.path.text
        self.path = self.path.strip()
        self.path = self.path.replace('"','')