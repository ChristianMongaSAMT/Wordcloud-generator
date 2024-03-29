from collections import OrderedDict
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger

class ImportantWords(BoxLayout):
    txt = StringProperty()
    wordsOrderByEmphasis = {}
    words = ""
    def __init__(self, row, **kwargs):
        super(ImportantWords, self).__init__(**kwargs)
        self.txt = row

    def orderByEmphasis(self, words, wordsOrderByEmphasis):
        self.words = words
        # Ordina le parole per la loro enfasi
        self.wordsOrderByEmphasis = wordsOrderByEmphasis
        for word in self.words:
            if(word != '' and word in self.wordsOrderByEmphasis):
                self.wordsOrderByEmphasis[word] += 1

        self.sortEmphasisWords()
        return self.wordsOrderByEmphasis
    
    def userEmphasis(self, wordsUser):
        # Inverte l'array mettendo alla prima posizione l'ultima parola scritta
        self.words = wordsUser
        self.words = self.words[::-1]
        print(self.words)

        for word in self.words:
            if(word != ''):
                # Prende il valore più alto e lo usa per impostare l'enfasi della parola inserita dall'utente che sarà più grande di 1
                self.wordsOrderByEmphasis[word] = list(self.wordsOrderByEmphasis.values())[-1] + 1 #[-1]  parte dalla fine

                # Ordina l'array
                self.sortEmphasisWords()
        return self.wordsOrderByEmphasis

    def sortEmphasisWords(self):
        self.wordsOrderByEmphasis = OrderedDict(sorted(self.wordsOrderByEmphasis.items(), key=lambda x: x[1], reverse=False))#TRUE DAL PIÙ GRANDE AL PIÙ PICCOLO
        Logger.info(f'[importantwords.py] ordinata variabile per enfasi contenente le parole')