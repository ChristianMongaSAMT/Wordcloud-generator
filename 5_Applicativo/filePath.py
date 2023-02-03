
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

logmanager.get_configured_logger()

########################DragNDrop############################
class WindowFileDropExampleApp(App):
    def build(self):
        Window.bind(on_drop_file=self._on_file_drop)
        return Label(text = "Drag and Drop File here")

    def _on_file_drop(self, window, file_path,x ,y):
        fp = open(file_path, 'r')
        print(fp.read())
        return

####################################################################
if __name__ == '__main__':
    WindowFileDropExampleApp().run()
