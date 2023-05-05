from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.text import LabelBase

from kivy.logger import Logger


#TO DO: da mettere i font nella cartella
FONT_MAPPING = {}
FONT_MAPPING['Cartoon'] = './fonts/from-cartoon-blocks/From Cartoon Blocks.ttf'
FONT_MAPPING['Borex'] = './fonts/borex/BOREX-Regular.otf'
FONT_MAPPING['Krinkes'] = './fonts/krinkes/KrinkesRegularPERSONAL.ttf'
FONT_MAPPING['Theaters'] = './fonts/theaters/THEATERS DEMO REGULAR.ttf'
FONT_MAPPING['Calibri'] = './fonts/calibri/Calibri.ttf'
FONT_MAPPING['Roboto'] = './data/fonts/Roboto-Regular.ttf'

font = "./fonts/borex/BOREX-Regular.otf"
def getFont():
    return font
for font_name, font_path in FONT_MAPPING.items():
    LabelBase.register(name=font_name, fn_regular=font_path)  

class FontFamily(BoxLayout):
    txt = StringProperty()
    
    def __init__(self, row, **kwargs):
        super(FontFamily, self).__init__(**kwargs)
        self.txt = row
    
    def font_changed(self):
        # Memorizza il nuovo font
        global font
        font = self.ids.fontSpinner.text
        font = FONT_MAPPING[font]
        Logger.info(f'[fontselector.py] selezionato font: {font}')
        # (Test) Applica il font al label
        self.ids.fontLabel.font_name = font