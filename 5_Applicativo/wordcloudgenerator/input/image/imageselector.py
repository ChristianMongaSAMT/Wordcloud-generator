from argparse import FileType
import filetype
import os
import queue

from event import post_event

from kivy.uix.widget import Widget

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

path = './pictures/stellina.jpg'
q = queue.Queue() #global messages
q.put('./pictures/default.png')

def getQueue():
    val = None
    try:
        val = q.get_nowait()
    except Exception as e:
        pass
    return val


def getPath():
    return path

def setPath(newPath):
    global path
    path = newPath

class ImageSelector(BoxLayout, Widget):
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

    '''def setPasfsdfth(self):
        # Controlla se è una path valida, se la path è un file e se è un'immagine
        
        if(not (os.path.exists(path) and os.path.isfile(path) and FileType.is_image(path))):
            self.imagepath = './pictures/default.png'
        else:
            self.imagepath = path'''

    def visualizer(self):
        global q
        global path
        # Memorizza la nuova path
        self.getPathFromTextInput()
        if((os.path.exists(getPath()) and os.path.isfile(getPath()) and filetype.is_image(getPath()))):
            # Se la path esiste la usa per l'immagine
            #imageSource = self.path
            print('valid path')
            print(f'putting in queue: {path}')
            q.put(path)
            print(f'queue size: {q.qsize()}')
        else:
            # Se la path non esiste carica l'immagine di default
            path = './pictures/default.png'
        
        

        #print(q.get())
        
    def getPathFromTextInput(self):
        # Prende la path per l'immagine dal text input
        path = self.ids.path.text
        path = path.strip()
        path = path.replace('"','')
        setPath(path)