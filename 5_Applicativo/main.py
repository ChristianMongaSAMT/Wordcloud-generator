import os
import cv2
import validators
import filetype
import array

from bs4 import BeautifulSoup
import kivy
from kivy.config import Config
from kivy.logger import Logger
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from urllib.request import urlopen
from collections import OrderedDict
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#from kivy.properties import ObjectProperty
#from kivy.lang import Builder
#from kivy.core.text import _default_font_paths
#from kivy.properties import StringProperty
from kivy.core.window import Window

Config.read('./config.ini')

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
        

FONT_MAPPING = {}
FONT_MAPPING['Cartoon'] = './fonts/from-cartoon-blocks/From Cartoon Blocks.ttf'
FONT_MAPPING['Borex'] = './fonts/borex/BOREX-Regular.otf'
FONT_MAPPING['Krinkes'] = './fonts/krinkes/KrinkesRegularPERSONAL.ttf'
FONT_MAPPING['Theaters'] = './fonts/theaters/THEATERS DEMO REGULAR.ttf'

for font_name, font_path in FONT_MAPPING.items():
    LabelBase.register(name=font_name, fn_regular=font_path)    

class WordCloudApp(App):
    path = './pictures/default.png'
    wordsOrderByEmphasis = {}
    sm = ScreenManager()
    font = ""

    words = ""
    excludedWords = ""
    userExcludedWords = ""
    isWordValid = True
    
    # Dizionario
    
    proxySetup = []
    isProxySetup = False

    def build(self):
        self.createScenes()
        return self.sm

    def createScenes(self):
        # Creazione scene
        self.sm.add_widget(WordCloudGUI(name='gui'))
        self.sm.add_widget(DownloadScreen(name='download'))
        self.sm.add_widget(ImageModifier(name='image'))


    def getPathFromTextInput(self):
        # Prende la path per l'immagine dal text input
        self.path = self.root.get_screen('gui').ids.path.text
        self.path = self.path.strip()
        self.path = self.path.replace('"','')
        
    def visualizer(self):
        # Memorizza la nuova path
        self.getPathFromTextInput()

        if(not ((os.path.exists(self.path) and os.path.isfile(self.path) and filetype.is_image(self.path)))):
            # Se la path non esiste carica l'immagine di default
            self.root.get_screen('gui').ids.image.source = './pictures/default.png'
        else:
            # Se la path esiste la usa per l'immagine
            self.root.get_screen('gui').ids.image.source = self.path

    def downloadImage(self):
        # Metodo per il download dell'immagine
        print('DOWNLOAD')

    def font_changed(self):
        # Memorizza il nuovo font
        self.font = self.root.get_screen('gui').ids.fontSpinner.text

        # (Test) Applica il font al label
        print(self.font)
        self.root.get_screen('gui').ids.fontLabel.font_name = self.font

    def changeToImageModifier(self):
        # Cambia scena impostanto quella dove si può modificare l'immagine base
        
        # Imposta il current screen come "image"
        self.sm.current = 'image' 
        
        # Memorizza la tolleranza
        tolerance = self.root.get_screen('image').ids.tolerance_slider.value
        
        #print(f'Tollerance: {tolerance}')

        #get current screen (read only) as Object (not name) and since it is an intance of ImageModifier it contains the updateImage method
        
        # Richiama il metodo in ImageModifier per aggiornare l'immagine
        self.sm.current_screen.updateImage(self.path, self, tolerance, self.font, self.wordsOrderByEmphasis)

    def getInputType(self):
        # Ritorna il tipo di input selezionato
        return self.root.get_screen('gui').ids.inputType.text

    def generateListWord(self):
        self.words = ''
        self.wordsOrderByEmphasis = {}
        self.excludedWords = list(open('./text/excludedWords.txt', 'r').read().rsplit(','))
        self.initUserExcludedWords()
        print(self.excludedWords)
        inputType = self.getInputType()
        
        # Controlla il tipo di input e in base a quello memorizza le parole
        if(inputType == 'FILE'):
            self.getWordsFromFile()
        elif(inputType == 'URL'):
            self.getWordsFromUrl()
        else:
            self.getWordsFromText()
        
        # Controlla le parole
        self.checkWords(self.words)
        
        # Memorizza l'enfasi delle parole
        self.orderByEmphasis()

        self.userEmphasis()
          
    def areLetters(self, words):
        for character in words:    
            # isalpha accetta anche i caratteri speiali come "?", "!", "@"
            # isalpha  or  (character >= 'a' and character <= 'z' or character >= 'A' and character <= 'Z')
            if(not(character >= 'a' and character <= 'z' or character >= 'A' and character <= 'Z')):
                words = words.replace(character, ' ')
        return words

    def checkWords(self, wordsToCheck):
        self.words = wordsToCheck
        # Ciclo per escludere i carattero speciali
        self.words = self.areLetters(self.words)
        
        # Se words contiene qualcosa 
        if(len(self.words) > 0):
            # Separa le parole
            self.words = self.words.rsplit(" ")

            # Controlla singolarmente ogni parola
            for word in self.words:
                if(word != ''):
                    # Controlla se la parola scritta è contenuta nelle parole escluse
                    for excludedWord in self.excludedWords:
                        if(word.lower() == excludedWord.lower()):
                            self.isWordValid = False
                    # Se la parola è valida la inserisce nell'array
                    if(self.isWordValid):
                        if (word not in self.wordsOrderByEmphasis):
                            self.wordsOrderByEmphasis[word] = 0
                self.isWordValid = True
                
    def getWordsFromText(self):
        # Prende le parole dal testo inserito
        self.words =  self.root.get_screen('gui').ids.pathWords.text

    def getWordsFromFile(self):
        # Memorizza la path del file
        wordFile = self.root.get_screen('gui').ids.pathWords.text

        # Controlla se la path è un file
        if(os.path.isfile(wordFile)):
            # Legge e salva le parole contenute nel file
            self.words = open(wordFile, 'r').read()

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
                if(name.upper() == 'HTTP_PROXY' or name.upper() == 'HTTPS_PROXY'):
                    self.proxySetup.append(f"{name}: {value}")
            self.isProxySetup = True
            print(self.proxySetup)

    def removeTags(self, html):
        # Tramite BeautifulSoup vengono rimossi tutti i tag della pagina web e viene formattato il testo
        pageParsed = BeautifulSoup(html, 'html.parser')
        for data in pageParsed(['style', 'script']):
            data.decompose()
        return ' '.join(pageParsed.stripped_strings)

    def orderByEmphasis(self):
        # Ordina le parole per la loro enfasi
        for word in self.words:
            if(word != '' and word in self.wordsOrderByEmphasis):
                self.wordsOrderByEmphasis[word] += 1

        self.sortEmphasisWords()
    
    def userEmphasis(self):
        words = self.root.get_screen('gui').ids.importantWords.text
        # Controlla le parole inserite dall'utente
        self.checkWords(words)
        # Inverte l'array mettendo alla prima posizione l'ultima parola scritta
        self.words = self.words[::-1]
        print(self.words)

        for word in self.words:
            if(word != ''):
                # Prende il valore più alto e lo usa per impostare l'enfasi della parola inserita dall'utente che sarà più grande di 1
                self.wordsOrderByEmphasis[word] = list(self.wordsOrderByEmphasis.values())[0] + 1

                # Ordina l'array
                self.sortEmphasisWords()

        print("---")
        for index in self.wordsOrderByEmphasis:
            print(f"{index}: {self.wordsOrderByEmphasis[index]}")
        print("---")
    
    def initUserExcludedWords(self):
        exWords = self.root.get_screen('gui').ids.excludedWords.text
        exWords = self.areLetters(exWords)
        exWords = exWords.rsplit(" ")

        for word in exWords:
            self.excludedWords.append(word)

    def sortEmphasisWords(self):
        self.wordsOrderByEmphasis = OrderedDict(sorted(self.wordsOrderByEmphasis.items(), key=lambda x: x[1], reverse=False))#TRUE DAL PIÙ GRANDE AL PIÙ PICCOLO

class DownloadScreen(Screen):
    pass

class ImageModifier(Screen, BoxLayout):
    
    def updateImage(self, path, wcApp, tolerance, font,wordsOrderByEmphasis):
        self.wcApp = wcApp
        self.setPath(path)
        self.createBorderImage(tolerance, font, wordsOrderByEmphasis)

        tolPer = int((self.ids.tolerance_slider.value / 2000) * 100)
        tolValue = f'Tolerance: {str(tolPer)}%'
        self.ids.tolerance_label.text = tolValue

    def setPath(self, path):
        # Controlla se è una path valida, se la path è un file e se è un'immagine
        if(not (os.path.exists(path) and os.path.isfile(path) and filetype.is_image(path))):
            self.imagepath = './pictures/default.png'
        else:
            self.imagepath = path

    def printAllWords(self, img, font, pathTempImage, wordsOrderByEmphasis):
        img = Image.open(pathTempImage)
        fontSize = 20
        # Moltiplicatore
        k = 1.5 
        for key, word in enumerate(wordsOrderByEmphasis):
            # Creo un immagine da sovrappore trasparente
            myFont = ImageFont.truetype(FONT_MAPPING[font] , int(fontSize * (key+1) * k))
            tim = Image.new('RGBA', (500,200), (0,0,0,0))
            I1 = ImageDraw.Draw(tim)

            I1.text((0,0), word, font=myFont, fill=(0,0,255))
            print("starei ruotando")
            if(key % 2 == 0):
                tim = tim.rotate(90,  expand=1)
                img.paste(tim, (key * 28, 50), tim)

            else:
                tim = tim.rotate(0,  expand=1)
                img.paste(tim, (28, key * 50), tim)

        img.save(pathTempImage)
        
    def createBorderImage(self, tolerance, font, wordsOrderByEmphasis):
        #Logger.info(f'createBorderImage with: {tolerance} on image {self.imagepath}')

        # Legge l'immagine corrispondente alla path
        img = cv2.imread(self.imagepath)

        # Converte l'immagine ad una scala di grigi
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Applica il thresholding nell'immagine grigia per avere un'immagine binaria
        ret,thresh = cv2.threshold(gray,150,255,0)

        # Trova il contorno usando l'immagine binaria
        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            # Per ogni contorno calcola area e perimetro
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            perimeter = round(perimeter, 4)

            # Se l'area è maggiore ad un determinato numero la disegna sull'immagine
            if(area > tolerance):
                cv2.drawContours(img, [cnt], -1, (0,0,255), 2)

        # Crea una nuova immagine che conterrà i bordi
        pathTempImage = './pictures/imageMod.png'
        cv2.imwrite(pathTempImage, img)

        self.printAllWords(img, font, pathTempImage, wordsOrderByEmphasis)

        # Imposta la path nell'Image
        self.ids.imageMod.source = pathTempImage
        Logger.info(f'imageMod: {self.ids.imageMod.source}')

        # Ricarice l'immagine
        self.ids.imageMod.reload()

if __name__ == '__main__':
    Window.fullscreen = 'auto'
    WordCloudApp().run()