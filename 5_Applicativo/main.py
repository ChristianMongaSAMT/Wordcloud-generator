import kivy
import logging
import os

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

    def build(self):
        sm = ScreenManager()
        sm.add_widget(WordCloudGUI(name='gui'))
        sm.add_widget(DownloadScreen(name='download'))

        LabelBase.register(name='Cartoon',
                   fn_regular='./fonts/from-cartoon-blocks/From Cartoon Blocks.ttf')
        LabelBase.register(name='Borex',
                   fn_regular='./fonts/borex/BOREX-Regular.otf')
        LabelBase.register(name='Krinkes',
                   fn_regular='./fonts/krinkes/KrinkesRegularPERSONAL.ttf')
        LabelBase.register(name='Theaters',
                   fn_regular='./fonts/theaters/THEATERS DEMO REGULAR.ttf')
        
        return sm

    def process(self):
        self.path = self.root.get_screen('gui').ids.path.text
        print(os.getcwd())
        
        print(self.path)

    def visualizer(self):
        self.process()
        if(os.path.exists(self.path)):
            self.root.get_screen('gui').ids.image.source = self.path

    def downloadImage(self):
        print("DOWNLOAD")

    def font_changed(self):
        font = self.root.get_screen('gui').ids.fontSpinner.text
        self.root.get_screen('gui').ids.fontLabel.font_name = font


class DownloadScreen(Screen):
    pass

# def run():
    

if __name__ == '__main__':
    WordCloudApp().run()
    