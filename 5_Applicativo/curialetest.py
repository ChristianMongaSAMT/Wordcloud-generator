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
import re
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

Config.read('./config.ini')

class CurialeGUI(BoxLayout): 
    pass

class CurialeApp(App):
    path = "./pictures/class.png"
    words = ""
    excludedWords = open("./text/excludedWords.txt", "r").read().rsplit(",")
    isWordValid = True


    
    def remove_tags(html):
        soup = BeautifulSoup(html, "html.parser")
        for data in soup(['style', 'script']):
            data.decompose()
        return ' '.join(soup.stripped_strings)
 
    
    link = "https://stackoverflow.com/questions/15138614/how-can-i-read-the-contents-of-an-url-with-python"
    #proxy_env = os.environ['JAVA_HOME']
    #print("ENV:", proxy_env)
    for name, value in os.environ.items():
        print("{0}: {1}".format(name, value))
    #f = urlopen(link)
    #myfile = f.read()
    #print(remove_tags(myfile))

    def build(self):
        return CurialeGUI()

    def getWords(self):
        self.wordFile = self.root.ids.pathWords.text
        print(self.wordFile)
        if(os.path.isfile(self.wordFile)):
            self.words = open(self.wordFile, "r").read()
            

    def generateListWord(self, isFile):
        if(isFile):
            self.getWords()
        else:
            self.words =  self.root.ids.wordsList.text
        for character in self.words:
            #isalpha accetta anche i caratteri speiali come "?", "!", "@"
            #isalpha  or  (character >= 'a' and character <= 'z' or character >= 'A' and character <= 'Z')
            if(not(character >= 'a' and character <= 'z' or character >= 'A' and character <= 'Z')):
                self.words = self.words.replace(character, " ")
        if(len(self.words) > 0):
            print = ""
            self.words = self.words.rsplit(" ")
            for word in self.words:
                if(word != ""):
                    for excludedWord in self.excludedWords:
                        if(word.lower() == excludedWord.lower()):
                            self.isWordValid = False
                    if(self.isWordValid):
                        print += word + "\n"
                self.isWordValid = True
            self.root.ids.result.text = print


    def process(self):
        self.path = self.root.ids.path.text
        print(os.path.abspath(self.path))

    def visualizer(self):
        self.process()
        if(os.path.exists(self.path)):
            self.root.ids.image.source = self.path

if __name__ == '__main__':
    CurialeApp().run()
    