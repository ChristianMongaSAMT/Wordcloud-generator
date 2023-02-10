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


Config.read('./config.ini')



class CurialeGUI(BoxLayout): 
    pass

class CurialeApp(App):
    path = "./pictures/class.png"

    def build(self):
        return CurialeGUI()

    def process(self):
        self.path = self.root.ids.path.text
        print(self.path)

    def visualizer(self):
        self.process()
        if(os.path.exists(self.path)):
            self.root.ids.image.source = self.path

if __name__ == '__main__':
    CurialeApp().run()
    