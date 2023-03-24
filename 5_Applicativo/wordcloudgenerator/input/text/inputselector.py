import os
import validators
import tkinter as tk
from tkinter import filedialog

from bs4 import BeautifulSoup
from urllib.request import urlopen
from kivy.uix.screenmanager import ScreenManager

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

from input.text.helpertextinput import helperTextInput

class InputType(BoxLayout):
    path = './pictures/default.png'
    wordsOrderByEmphasis = {}
    sm = ScreenManager()
    font = ""

    words = ""
    excludedWords = ""
    userExcludedWords = ""
    isWordValid = True
    

    

    txt = StringProperty()
    important = 0
    excluded = 0
    fontFamily = 0
    hp = helperTextInput()
    def __init__(self, important, excluded, fontFamily,  row,**kwargs):
        super(InputType, self).__init__(**kwargs)
        self.txt = row
        self.important = important
        self.excluded = excluded
        self.fontFamily = fontFamily

    def getInputType(self):
        # Ritorna il tipo di input selezionato
        return self.ids.inputType.text

    def generateListWord(self):
        self.words = ''
        self.wordsOrderByEmphasis = {}
        self.excludedWords = list(open('./text/excludedWords.txt', 'r').read().rsplit(','))
        self.excludedWords = self.excluded.initUserExcludedWords(self.excludedWords)
        print(self.excludedWords)
        inputType = self.getInputType()
        
        # Controlla il tipo di input e in base a quello memorizza le parole
        if(inputType == 'FILE'):
            self.ids.pathWords.text = self.get_path()
            self.getWordsFromFile()
        elif(inputType == 'URL'):
            self.getWordsFromUrl()
        else:
            self.getWordsFromText()
        
        # Controlla le parole
        self.checkWords(self.words)

        print(self.words)
        
        # Memorizza l'enfasi delle parole
        self.wordsOrderByEmphasis = self.important.orderByEmphasis(self.words, self.wordsOrderByEmphasis)

        # Controlla le parole dell'enfasi inserite dall'utente
        self.words = self.important.ids.importantWords.text
        self.checkWords(self.words)
        self.wordsOrderByEmphasis = self.important.userEmphasis(self.words)

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
        self.hp.setProxyIfExist()

        # Salva il link 
        link = self.ids.pathWords.text

        # Se il link è valido salva le parole della pagina web
        if(validators.url(link)):
            webPage = urlopen(link)
            textFromWebPage = webPage.read()
            self.words = str(self.hp.removeTags(textFromWebPage))

    def checkWords(self, wordsToCheck):
        self.words = wordsToCheck
        # Ciclo per escludere i carattero speciali
        self.words = self.excluded.areLetters(self.words)
        
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

    @staticmethod
    def get_path():
        root = tk.Tk()
        root.withdraw()

        return( filedialog.askopenfilename() )