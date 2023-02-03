import kivy
import logging
import logmanager

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout



logmanager.get_configured_logger()

class WordCloudGUI(BoxLayout):
    pass

class WordCloudApp(App):
    def build(self):
        return WordCloudGUI()

"""
class Coso():

     b = None

    _c = None

    def __init__(self, params):
        self.a = params

    def get_a(self) -> str:
        return self.a

    def set_a(self, value):
        self.a = value


    def set_fkljdsjfkls(self, v1, v2='0000'):
        self.v1 = v1
        self.v2 = v2
"""
# def run():
    

if __name__ == '__main__':
    WordCloudApp().run()