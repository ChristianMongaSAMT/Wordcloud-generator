from kivy.uix.button import Button
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.properties import StringProperty
import logging
import kivy
from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.lang import Builder
from pathlib import Path
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import _default_font_paths

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
        fontFam = FontFam()
        LabelBase.register(name='Cartoon',
                   fn_regular='E:/306/Worldcloud-generatorData/fonts/from-cartoon-blocks/From Cartoon Blocks.ttf')
        LabelBase.register(name='Borex',
                   fn_regular='E:/306/Worldcloud-generatorData/fonts/borex/BOREX-Regular.otf')
        LabelBase.register(name='Krinkes',
                   fn_regular='E:/306/Worldcloud-generatorData/fonts/krinkes/KrinkesRegularPERSONAL.ttf')
        LabelBase.register(name='Theaters',
                   fn_regular='E:/306/Worldcloud-generatorData/fonts/theaters/THEATERS DEMO REGULAR.ttf')
        return fontFam

    def getText(self):
        text = self.root.ids.perro.text
        text = self.root.ids.fontLabel.text
        print(_default_font_paths)
        print(text)

    def font_changed(self):
        font = self.root.ids.fontSpinner.text
        self.root.ids.fontLabel.font_name = font

if __name__ == '__main__':
    #WindowFileDropExampleApp().run()
    f = fontfamilyApp()
    f.run()