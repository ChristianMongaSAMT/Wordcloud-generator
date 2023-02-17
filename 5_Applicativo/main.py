import kivy
import logging
import os
import cv2
import urllib.request

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
from urllib.request import urlopen

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
    sm = ScreenManager()

    def build(self):
        
        self.sm.add_widget(WordCloudGUI(name='gui'))
        self.sm.add_widget(DownloadScreen(name='download'))
        self.sm.add_widget(ImageModifier(name='image'))

        LabelBase.register(name='Cartoon', fn_regular='./fonts/from-cartoon-blocks/From Cartoon Blocks.ttf')
        LabelBase.register(name='Borex', fn_regular='./fonts/borex/BOREX-Regular.otf')
        LabelBase.register(name='Krinkes', fn_regular='./fonts/krinkes/KrinkesRegularPERSONAL.ttf')
        LabelBase.register(name='Theaters', fn_regular='./fonts/theaters/THEATERS DEMO REGULAR.ttf')

        return self.sm

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

    def change(self):
        self.sm.current = "image"
        ImageModifier.build(self.path, self)

    '''
    def remove_tags(html):
        soup = BeautifulSoup(html, "html.parser")
        for data in soup(['style', 'script']):
            data.decompose()
        return ' '.join(soup.stripped_strings)
 
    link = "https://stackoverflow.com/questions/15138614/how-can-i-read-the-contents-of-an-url-with-python"
    f = urlopen(link)
    myfile = f.read()
    print(remove_tags(myfile))
    '''


class DownloadScreen(Screen):
    pass

class ImageModifier(Screen):
    def build(path, wcApp):
        # Read the input image
        img = cv2.imread(path)

        # convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply thresholding in the gray image to create a binary image
        ret,thresh = cv2.threshold(gray,150,255,0)

        # Find the contours using binary image
        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        print("Number of contours in image:",len(contours))
        for cnt in contours:
            # compute the area and perimeter
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            perimeter = round(perimeter, 4)

            if(area > 1000):
                print('Area:', area)
                print('Perimeter:', perimeter)
                cv2.drawContours(img, [cnt], -1, (0,0,255), 3)
                #x1, y1 = cnt[0,0]

        #wcApp.root.get_screen('image').ids.imageMod.texture = img
        cv2.imwrite('modificata.png', img)
        #wcApp.root.get_screen('image').ids.imageMod.source = 'prova.png'
        wcApp.root.get_screen('image').ids.imageMod.source = 'modificata.png'
        

        #wcApp.root.get_screen('gui').ids.image.source = path
        #cv2.imshow("Image", img)    
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        pass

if __name__ == '__main__':
    WordCloudApp().run()
    