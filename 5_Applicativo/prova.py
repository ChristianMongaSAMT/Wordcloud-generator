
import logging
import logmanager
import kivy
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.lang import Builder
from pathlib import Path


logmanager.get_configured_logger()

class Test():   
    folder = ""

    def __init__(self, path):
        self.folder = Path(path)

    def printData(self):
        logging.debug(f'{self.folder.read_text()}')
        
class DragLabel(DragBehavior, Label):
    pass

class TestApp(App):

    def build(self):
        self.title = 'ztest'


#def run():
#    test = Test('E:\\306\\Worldcloud-generatorData\\testingPath.txt')
#    test.printData()

if __name__ == '__main__':
    TestApp().run()