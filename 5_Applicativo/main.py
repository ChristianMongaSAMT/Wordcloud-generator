import kivy
import logging
import logmanager

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window


logmanager.get_configured_logger()
# __drag and drop__ 
class DragAndDrop():
    def build(self):
        Window.bind(on_drop_file=self._on_file_drop)
        return Label(text = "Drag and Drop File here")

    def _on_file_drop(self, window, file_path,x ,y):
        fp = open(file_path, 'r')
        print(fp.read())
        return

class WordCloudGUI(BoxLayout):
    pass

class WordCloudApp(App):
    def build(self):
        return WordCloudGUI()

# def run():
    

if __name__ == '__main__':
    WordCloudApp().run()