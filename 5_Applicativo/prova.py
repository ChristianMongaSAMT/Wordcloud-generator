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
from kivy.graphics import *
import cv2
import numpy as np

########################DragNDrop############################
class WindowFileDropExampleApp(App):
    def build(self):
        Window.bind(on_drop_file=self._on_file_drop)
        return

    def _on_file_drop(self, window, file_path, x, y):
        #logging.debug(f'file: {file_path}, drop location ({x};{y})')
        text = Path(file_path.decode("utf-8")).read_text() #testo del file
        print(Path(file_path.decode("utf-8")))
####################################################################
class FontFam(BoxLayout):
    pass

class fontfamilyApp(App):
    def build(self):      
        fontFam = FontFam()
        
        #fL = fontFam.ids.fontLabel
        #fL.bind(on_drop_file=self._on_file_drop)
        #self._on_file_drop
        LabelBase.register(name='Cartoon',
                   fn_regular='E:/306/Worldcloud-generatorData/fonts/from-cartoon-blocks/From Cartoon Blocks.ttf')
        LabelBase.register(name='Borex',
                   fn_regular='E:/306/Worldcloud-generatorData/fonts/borex/BOREX-Regular.otf')
        LabelBase.register(name='Krinkes',
                   fn_regular='E:/306/Worldcloud-generatorData/fonts/krinkes/KrinkesRegularPERSONAL.ttf')
        LabelBase.register(name='Theaters',
                   fn_regular='E:/306/Worldcloud-generatorData/fonts/theaters/THEATERS DEMO REGULAR.ttf')
        self.build_image
        """with fontFam.canvas:
            # Add a red color
            Color(1., 0, 0)

            # Add a rectangle
            Ellipse(pos=(10,10), size=(500, 500))"""


        return fontFam

    def getText(self):
        text = self.root.ids.perro.text
        text = self.root.ids.fontLabel.text
        print(text)

    def font_changed(self):
        font = self.root.ids.fontSpinner.text
        self.root.ids.fontLabel.font_name = font

    def _on_file_drop(self, window, file_path, x, y):
        #logging.debug(f'file: {file_path}, drop location ({x};{y})')
        text = Path(file_path.decode("utf-8")).read_text() #testo del file
        print(Path(file_path.decode("utf-8")))

    def build_image(self):

        img = cv2.imread('./pictures/cubi.jpg')

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold(gray,150,255,0)

        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        print("Number of contours in image:",len(contours))
        for cnt in contours:
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            perimeter = round(perimeter, 4)

            if(area > 1000):
                print('Area:', area)
                print('Perimeter:', perimeter)
                cv2.drawContours(img, [cnt], -1, (0,0,255), 3)
                x1, y1 = cnt[0,0]

        cv2.imshow("Image", img)    
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    #WindowFileDropExampleApp().run()
    f = fontfamilyApp()
    f.run()
    
    