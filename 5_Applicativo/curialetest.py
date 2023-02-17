import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from pathlib import Path
from kivy.config import Config

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import validators

Config.read('./config.ini')

class CurialeGUI(BoxLayout): 
    pass

class CurialeApp(App):
    path = "./pictures/class.png"
    words = ""
    excludedWords = open("./text/excludedWords.txt", "r").read().rsplit(",")
    isWordValid = True
    proxySetup = []
    isProxySetup = False

    def build(self):
        return CurialeGUI()
    
    def remove_tags(self, html):
        soup = BeautifulSoup(html, "html.parser")
        for data in soup(['style', 'script']):
            data.decompose()
        return ' '.join(soup.stripped_strings)

    def setProxyIfExist(self):
        if(not(self.isProxySetup)):
            for name, value in os.environ.items():
                if(name.upper() == "HTTP_PROXY" or name.upper() == "HTTPS_PROXY"):
                    self.proxySetup.append(f"{name}: {value}")
                    print(f"{self.proxySetup}")
            self.isProxySetup = True


    def getWordsFromUri(self):
        self.setProxyIfExist()
        link = self.root.ids.pathUri.text
        if(validators.url(link)):
            f = urlopen(link)
            myfile = f.read()
            self.words = str(self.remove_tags(myfile))

    def getWords(self):
        self.wordFile = self.root.ids.pathWords.text
        print(self.wordFile)
        if(os.path.isfile(self.wordFile)):
            self.words = open(self.wordFile, "r").read()
            
    def generateListWord(self, type):
        if(type == "FILE"):
            self.getWords()
        elif(type == "URL"):
            self.getWordsFromUri()
        else:
            self.words =  self.root.ids.wordsList.text
        for character in self.words:
            
            #isalpha accetta anche i caratteri speiali come "?", "!", "@"
            #isalpha  or  (character >= 'a' and character <= 'z' or character >= 'A' and character <= 'Z')
            if(not(character >= 'a' and character <= 'z' or character >= 'A' and character <= 'Z')):
                self.words = self.words.replace(character, " ")
        if(len(self.words) > 0):
            printer = "ciao"
            self.words = self.words.rsplit(" ")
            for word in self.words:
                print(word)
                if(word != ""):
                    for excludedWord in self.excludedWords:
                        if(word.lower() == excludedWord.lower()):
                            self.isWordValid = False
                    if(self.isWordValid):
                        printer += word + "\n"
                self.isWordValid = True
            self.root.ids.result.text = printer


    def process(self):
        self.path = self.root.ids.path.text
        print(os.path.abspath(self.path))

    def visualizer(self):
        self.process()
        if(os.path.exists(self.path)):
            self.root.ids.image.source = self.path

if __name__ == '__main__':
    CurialeApp().run()
    