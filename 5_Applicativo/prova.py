
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

########################DragNDrop############################
class WindowFileDropExampleApp(App):
    def build(self):
        Window.bind(on_drop_file=self._on_file_drop)
        return

    def _on_file_drop(self, window, file_path, x, y):
        logging.debug(f'file: {file_path}, drop location ({x};{y})')

        print(Path(file_path.decode("utf-8")).read_text())

        return
####################################################################
class FontFam(BoxLayout):
    pass

class fontfamilyApp(App):
    def build(self):
        return FontFam()
    def getText(self):
        return self.ids['fontLabel'].text      


if __name__ == '__main__':
    #logmanager.get_configured_logger()
    #WindowFileDropExampleApp().run()
    f = fontfamilyApp()
    print(f.getText())
    #fontfamilyApp().run()
