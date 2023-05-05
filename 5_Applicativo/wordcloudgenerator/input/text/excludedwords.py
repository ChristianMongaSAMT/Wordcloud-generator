from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from kivy.logger import Logger

class ExcludedWords(BoxLayout, object):
    txt = StringProperty()
    
    def __init__(self, row, **kwargs):
        super(ExcludedWords, self).__init__(**kwargs)
        self.txt = row

    
    def initUserExcludedWords(self, excludedWords):
        #print(self)
        userExWords = self.ids.excludedWords.text
        userExWords = self.areLetters(userExWords)
        userExWords = userExWords.rsplit(" ")
        Logger.info(f'[excludedwords.py] prese parole da escludere:{userExWords}')
        for word in userExWords:
            excludedWords.append(word)
        
        return excludedWords
    
    def areLetters(self, words):
        for character in words:    
            # isalpha accetta anche i caratteri speiali come "?", "!", "@"
            if(not(character >= 'a' and character <= 'z' or character >= 'A' and character <= 'Z')):
                words = words.replace(character, ' ')
        return words