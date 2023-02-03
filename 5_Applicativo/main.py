import kivy
import logging
import logmanager

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
from pathlib import Path
from kivy.config import Config


logmanager.get_configured_logger()
Config.read('./config.ini')

class TestRead():   

    def __init__(self, path):
        logging.debug(path.__class__)

        self.p = Path(path)

    def printData(self):
        logging.debug(f'{self.p.read_text()}')

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
class WordCloudGUI(BoxLayout):
    pTemp = "PERCORSO DA INSERIRE"
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

class WordCloudApp(App):
    def build(self):
        return WordCloudGUI()


     
        

# def run():
    

if __name__ == '__main__':
    WordCloudApp().run()
    