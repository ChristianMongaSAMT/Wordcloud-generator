import os
import cv2
import validators
import filetype

from bs4 import BeautifulSoup
from urllib.request import urlopen
from kivy.core.text import LabelBase

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder


ROWS = ["Input Type", "Important Words", "Excluded Words", "Font Family"]

FONT_MAPPING = {}
FONT_MAPPING['Cartoon'] = './fonts/from-cartoon-blocks/From Cartoon Blocks.ttf'
FONT_MAPPING['Borex'] = './fonts/borex/BOREX-Regular.otf'
FONT_MAPPING['Krinkes'] = './fonts/krinkes/KrinkesRegularPERSONAL.ttf'
FONT_MAPPING['Theaters'] = './fonts/theaters/THEATERS DEMO REGULAR.ttf'

for font_name, font_path in FONT_MAPPING.items():
    LabelBase.register(name=font_name, fn_regular=font_path)  

Builder.load_string("""

<MongaGUI>:
    ScrollView:
        Table:
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
            spacing: 50
    Image:
        id: image
        source: './pictures/stellina.jpg'


<InputType>:
    size_hint_y: None
    BoxLayout:
        orientation: 'horizontal'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: root.txt
            Spinner:
                id: inputType
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                text: 'LIST'
                values: 'FILE', 'LIST', 'URL'
        BoxLayout:
            orientation: 'vertical'
            TextInput:
                id: pathWords
                hint_text: "Insert input"
            Button:
                text: 'Send'
                on_release: root.generateListWord()

<ExcludedWords>:
    size_hint_y: None
    size_hint_x: 1
    height: 100
    Label:
        text: root.txt
    TextInput:
        id: excludedWords
        hint_text: root.txt
        
<ImportantWords>:
    size_hint_y: None
    size_hint_x: 1
    height: 100
    Label:
        text: root.txt
    TextInput:
        id: importantWords
        hint_text: root.txt

<FontFamily>:
    size_hint_y: None
    size_hint_x: 1
    height: 100
    Label:
        text: 'Font Family'
        id: fontLabel
        font_size: '20sp'
        text_size: self.size
        size_hint: 1, 0.3
    Spinner:
        text_size: self.size
        text: 'Font'
        values: 'Cartoon','Borex','Krinkes','Theaters','Calibri','Roboto'
        id: fontSpinner
        on_text:
            root.font_changed()
""")

class Table(BoxLayout):
    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        self.add_widget(InputType(ROWS[0]))
        self.add_widget(ImportantWords(ROWS[1]))
        self.add_widget(ExcludedWords(ROWS[2]))
        self.add_widget(FontFamily(ROWS[3]))

class InputType(BoxLayout):
    path = './pictures/default.png'
    wordsOrderByEmphasis = {}
    #sm = ScreenManager()
    font = ""

    words = ""
    excludedWords = ""
    userExcludedWords = ""
    isWordValid = True
    
    # Dizionario
    
    proxySetup = []
    isProxySetup = False
    txt = StringProperty()

    def __init__(self, row, **kwargs):
        super(InputType, self).__init__(**kwargs)
        self.txt = row

    def getInputType(self):
        # Ritorna il tipo di input selezionato
        return self.ids.inputType.text

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

        print(self.words)
        
        # Memorizza l'enfasi delle parole
        #self.orderByEmphasis()

        #self.userEmphasis()

    def getWordsFromText(self):
        # Prende le parole dal testo inserito
        self.words =  self.ids.pathWords.text

    def getWordsFromFile(self):
        # Memorizza la path del file
        wordFile = self.ids.pathWords.text

        # Controlla se la path è un file
        if(os.path.isfile(wordFile)):
            # Legge e salva le parole contenute nel file
            self.words = open(wordFile, 'r').read()

    def getWordsFromUrl(self):
        # Controlla se deve essere impostato un proxy
        self.setProxyIfExist()

        # Salva il link 
        link = self.root.ids.pathWords.text

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


class ImportantWords(BoxLayout):
    txt = StringProperty()
    
    def __init__(self, row, **kwargs):
        super(ImportantWords, self).__init__(**kwargs)
        self.txt = row

class ExcludedWords(BoxLayout):
    txt = StringProperty()
    
    def __init__(self, row, **kwargs):
        super(ExcludedWords, self).__init__(**kwargs)
        self.txt = row

class FontFamily(BoxLayout):
    txt = StringProperty()
    
    def __init__(self, row, **kwargs):
        super(FontFamily, self).__init__(**kwargs)
        self.txt = row
    
    def font_changed(self):
        # Memorizza il nuovo font
        self.font = self.ids.fontSpinner.text

        # (Test) Applica il font al label
        print(self.font)
        self.ids.fontLabel.font_name = self.font

class MongaGUI(BoxLayout):
    pass

class MongaApp(App):
    def build(self):
        mongaGUI = MongaGUI()
        return mongaGUI
    
if __name__ == '__main__':
    MongaApp().run()