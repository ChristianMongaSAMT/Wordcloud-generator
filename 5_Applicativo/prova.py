
import logging
import logmanager
import kivy
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.lang import Builder
from pathlib import Path
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.core.window import Window



class TestRead():   

    def __init__(self, path):
        logging.debug(path.__class__)
        print(f'path class: {path.__class__}')

        self.p = Path(path)

    def printData(self):
        logging.debug(f'{self.p.read_text()}')
        print(f'file content: {self.p.read_text()}')

########################DragNDrop############################
class WindowFileDropExampleApp(App):
    def build(self):
        Window.bind(on_drop_file=self._on_file_drop)
        return

    def _on_file_drop(self, window, file_path, x, y):
        logging.debug(f'file: {file_path}, drop location ({x};{y})')
        test = TestRead(file_path.decode("utf-8") )
        test.printData()
        return

####################################################################
if __name__ == '__main__':
    logmanager.get_configured_logger()
    WindowFileDropExampleApp().run()
