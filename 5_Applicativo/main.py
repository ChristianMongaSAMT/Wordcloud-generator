import kivy
import logging
import os
import cv2
import urllib.request
import validators
from bs4 import BeautifulSoup

from kivy.properties import StringProperty
from kivy.core.window import Window
from pathlib import Path
from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.text import _default_font_paths
from kivy.core.text import LabelBase
from urllib.request import urlopen

Config.read('./config.ini')

'''class TestRead():   

    def __init__(self, path):
        logging.debug(path.__class__)

        self.p = Path(path)

    def printData(self):
        logging.debug(f'{self.p.read_text()}')
'''
########################DragNDrop############################
'''class DragAndDrop():
    def build(self):
        Window.bind(on_drop_file=self._on_file_drop)
        #self.ids['l1'].bind(on_drop_file=self._on_file_drop)
        return

    def _on_file_drop(self, window, file_path, x, y):
        #logging.debug(f'file: {file_path}, drop location ({x};{y})')
        #test = TestRead(file_path.decode("utf-8") )
        print(f'drop {file_path.decode("utf-8")} location ({x},{y})')
        #Logger.info(f'drop {file_path.decode("utf-8")} location ({x},{y})')
        #test.printData()
        return
'''
class WordCloudGUI(BoxLayout, Screen):
    '''pTemp = "PERCORSO DA INSERIRE"
    #def __init__(self):
        #self.ids['l1'].text
    def build(self):
        self.ids['l1'].bind(on_drop_file=self._on_file_drop)

    def _on_file_drop(self, window, file_path, x, y):
        #logging.debug(f'file: {file_path}, drop location ({x};{y})')
        #test = TestRead(file_path.decode("utf-8") )
        print(f'drop {file_path.decode("utf-8")} location ({x},{y})')
        #Logger.info(f'drop {file_path.decode("utf-8")} location ({x},{y})')
        #test.printData()
        return   
    '''
    def build(self):
        pass
        


class WordCloudApp(App):
    path = "./pictures/class.png"
    sm = ScreenManager()

    words = ""
    excludedWords = open("./text/excludedWords.txt", "r").read().rsplit(",")
    isWordValid = True
    wordsOrderByEmphasis = {} #dizionario
    proxySetup = []
    isProxySetup = False

    def build(self):
        self.createScenes()
        self.registerFonts()
        return self.sm

    def createScenes(self):
        # Creazione scene
        self.sm.add_widget(WordCloudGUI(name='gui'))
        self.sm.add_widget(DownloadScreen(name='download'))
        self.sm.add_widget(ImageModifier(name='image'))

    def registerFonts(self):
        # Registrazione dei font
        LabelBase.register(name='Cartoon', fn_regular='./fonts/from-cartoon-blocks/From Cartoon Blocks.ttf')
        LabelBase.register(name='Borex', fn_regular='./fonts/borex/BOREX-Regular.otf')
        LabelBase.register(name='Krinkes', fn_regular='./fonts/krinkes/KrinkesRegularPERSONAL.ttf')
        LabelBase.register(name='Theaters', fn_regular='./fonts/theaters/THEATERS DEMO REGULAR.ttf')

    def getPathFromTextInput(self):
        # Prende la path per l'immagine dal text input
        self.path = self.root.get_screen('gui').ids.path.text

    def visualizer(self):
        # Memorizza la nuova path
        self.getPathFromTextInput()
        if(os.path.exists(self.path)):
            # Se la path esiste la usa per l'immagine
            self.root.get_screen('gui').ids.image.source = self.path

    def downloadImage(self):
        print("DOWNLOAD")

    def font_changed(self):
        # Memorizza il nuovo font
        font = self.root.get_screen('gui').ids.fontSpinner.text

        # (Test) Applica il font al label
        self.root.get_screen('gui').ids.fontLabel.font_name = font

    def changeToImageModifier(self):
        # Cambia scena impostanto quella dove si può scegliere cosa mantenere
        # dell'immagine e cosa no
        self.sm.current = "image"
        ImageModifier.build(self.path, self)

    def getInputType(self):
        # Ritorna il tipo di input selezionato
        return self.root.get_screen('gui').ids.inputType.text

    def generateListWord(self, type):
        self.words = ""
        # Controlla il tipo di input e in base a quello memorizza le parole
        if(type == "FILE"):
            self.getWordsFromFile()
        elif(type == "URL"):
            self.getWordsFromUrl()
        else:
            self.words =  self.root.get_screen('gui').ids.pathWords.text
        
        # Ciclo per escludere i carattero speciali
        for character in self.words:    
            #isalpha accetta anche i caratteri speiali come "?", "!", "@"
            #isalpha  or  (character >= 'a' and character <= 'z' or character >= 'A' and character <= 'Z')
            if(not(character >= 'a' and character <= 'z' or character >= 'A' and character <= 'Z')):
                self.words = self.words.replace(character, " ")
        # Se words contiene qualcosa 
        if(len(self.words) > 0):
            printer = ""

            # Separa le parole
            self.words = self.words.rsplit(" ")

            # Controlla singolarmente ogni parola
            for word in self.words:
                if(word != ""):
                    for excludedWord in self.excludedWords:
                        if(word.lower() == excludedWord.lower()):
                            self.isWordValid = False
                    if(self.isWordValid):
                        printer += word + "\n"
                self.isWordValid = True
                self.wordsOrderByEmphasis[word] = 0
            
            # Memorizza l'enfasi delle parole
            self.orderByEmphasis()  
    
    def getWordsFromFile(self):
        # Memorizza la path del file
        wordFile = self.root.get_screen('gui').ids.pathWords.text

        # Controlla se la path è un file
        if(os.path.isfile(wordFile)):
            # Legge e salva le parole contenute nel file
            self.words = open(wordFile, "r").read()

    def getWordsFromUrl(self):
        # Controlla se deve essere impostato un proxy
        self.setProxyIfExist()

        # Salva il link 
        link = self.root.get_screen('gui').ids.pathWords.text

        # Se il link è valido salva le parole della pagina web
        if(validators.url(link)):
            webPage = urlopen(link)
            textFromWebPage = webPage.read()
            self.words = str(self.removeTags(textFromWebPage))
    
    def setProxyIfExist(self):
        # Se non ci sono le variabili d'ambiente del proxy le aggiunge
        if(not(self.isProxySetup)):
            for name, value in os.environ.items():
                if(name.upper() == "HTTP_PROXY" or name.upper() == "HTTPS_PROXY"):
                    self.proxySetup.append(f"{name}: {value}")
            self.isProxySetup = True
            print(self.proxySetup)

    def removeTags(self, html):
        # Tramite BeautifulSoup vengono rimossi tutti i tag della pagina web e viene formattato il testo
        pageParsed = BeautifulSoup(html, "html.parser")
        for data in pageParsed(['style', 'script']):
            data.decompose()
        return ' '.join(pageParsed.stripped_strings)

    def orderByEmphasis(self):
        for word in self.words:
            self.wordsOrderByEmphasis[word] += 1

        #self.wordsOrderByEmphasis = sorted(self.wordsOrderByEmphasis) 
        
        for indice in self.wordsOrderByEmphasis:
            print(f"{indice}: {self.wordsOrderByEmphasis[indice]}")
        

class DownloadScreen(Screen):
    pass

class ImageModifier(Screen):
    def build(path, wcApp):
        # Legge l'immagine corrispondente alla path
        img = cv2.imread(path)

        # Converte l'immagine ad una scala di grigi
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Applica il thresholding nell'immagine grigia per avere un'immagine binaria
        thresh = cv2.threshold(gray,150,255,0)

        # Trova il contorno usando l'immagine binaria
        contours = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print("Number of contours in image:",len(contours))
        for cnt in contours:
            # Per ogni contorno calcola area e perimetro
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            perimeter = round(perimeter, 4)

            # Se l'area è maggiore ad un determinato numero la disegna sull'immagine
            if(area > 1000):
                #print('Area:', area)
                #print('Perimeter:', perimeter)
                cv2.drawContours(img, [cnt], -1, (0,0,255), 1)
                #x1, y1 = cnt[0,0]

        # Crea una nuova immagine che conterrà i bordi
        pathTempImage = path + '.png'
        cv2.imwrite(pathTempImage, img)
        wcApp.root.get_screen('image').ids.imageMod.source = pathTempImage
        
        #cv2.imshow("Image", img)    
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        pass

if __name__ == '__main__':
    WordCloudApp().run()
    